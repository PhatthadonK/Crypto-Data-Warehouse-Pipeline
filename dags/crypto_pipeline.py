from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
import pandas as pd
import json
import os
import boto3
from datetime import datetime

# --- CONFIG ---
DAG_ID = "crypto_etl_pipeline"
S3_BUCKET = "connect2databricks"
API_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"

# SECURE YOUR KEYS (Keep your existing keys here!)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

def extract_data():
    """Fetches data from CoinGecko API and uploads Raw JSON to S3"""
    print(f"🚀 Launching API Request to {API_URL}...")
    
    # Added User-Agent because CoinGecko sometimes blocks generic python scripts
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=20)
        response.raise_for_status() # Crash if API fails
        
        print("✅ API Success! Uploading to S3...")
        
        s3_client = boto3.client(
            "s3", 
            aws_access_key_id=AWS_ACCESS_KEY, 
            aws_secret_access_key=AWS_SECRET_KEY
        )

        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key="raw_crypto_data.json",
            Body=json.dumps(response.json()),
        )
        print("✅ Upload Successful to S3!")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        raise e

def process_data():
    """Reads JSON from S3, cleans with Pandas, loads to Postgres"""
    s3_client = boto3.client(
        "s3", 
        aws_access_key_id=AWS_ACCESS_KEY, 
        aws_secret_access_key=AWS_SECRET_KEY
    )

    print("📥 Downloading raw data from S3...")
    obj = s3_client.get_object(Bucket=S3_BUCKET, Key="raw_crypto_data.json")
    file_content = obj["Body"].read().decode("utf-8")
    json_data = json.loads(file_content)

    # --- NEW LOGIC FOR COINGECKO ---
    # CoinGecko returns a List directly, not a Dict with 'data'
    df = pd.DataFrame(json_data)

    # Map CoinGecko names to our SQL Schema
    # SQL: symbol, name, price_usd, volume_24h, rank
    rename_map = {
        'current_price': 'price_usd',
        'total_volume': 'volume_24h',
        'market_cap_rank': 'rank'
    }
    df.rename(columns=rename_map, inplace=True)
    
    # Select only the columns we need
    df = df[['symbol', 'name', 'price_usd', 'volume_24h', 'rank']]

    # Add Timestamp
    df["captured_at"] = datetime.now()

    print(f"✅ Transformed {len(df)} rows. Ready to Load.")
    print(df.head())

    # Load to Postgres
    pg_hook = PostgresHook(postgres_conn_id="postgres_dw")
    engine = pg_hook.get_sqlalchemy_engine()

    print("📤 Loading data to Postgres...")
    df.to_sql("crypto_prices", con=engine, if_exists="append", index=False)
    print("🏆 Data Loaded Successfully!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 0
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule='@hourly', 
    catchup=False,
) as dag:
    
    task1 = PythonOperator(task_id="extract_data", python_callable=extract_data)
    task2 = PythonOperator(task_id="process_data", python_callable=process_data)
    
    transform_task = BashOperator(
        task_id='dbt_transform',
        bash_command=(
            "python -m venv /tmp/dbt_env && "
            "source /tmp/dbt_env/bin/activate && "
            "pip install dbt-postgres && "

            "printf 'crypto_analytics:\n  target: dev\n  outputs:\n    dev:\n      type: postgres\n      host: postgres_dw\n      user: airflow\n      password: airflow\n      port: 5432\n      dbname: crypto_db\n      schema: public\n      threads: 1\n' > /opt/airflow/dbt/profiles.yml && "

            "cd /opt/airflow/dbt && "
            "dbt run --profiles-dir ."
        )
    )
    task1 >> task2 >> transform_task