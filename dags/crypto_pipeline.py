from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import requests
import pandas as pd
import json
import os
from datetime import datetime

# --- CONFIG ---
DAG_ID = "crypto_etl_pipeline"
S3_BUCKET = "connect2databricks" # Use your bucket name
API_URL = "https://api.coincap.io/v2/assets"

