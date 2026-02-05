## 📈 The Modern Crypto Data Stack
A robust, containerized Modern Data Stack pipeline. It extracts real-time cryptocurrency market data, stores raw history in a Data Lake (AWS S3), loads it into a Data Warehouse (PostgreSQL), transforms it using dbt, and visualizes it with Metabase.

## 🏗️ Architecture
Flow: CoinGecko API → Airflow (Extract) → AWS S3 (Data Lake) → PostgreSQL (Raw) → dbt (Transform) → Metabase (Visualize)

The pipeline consists of three major stages (ELT):

Extract & Load (EL): Airflow fetches live market data (Price, Volume, Rank) from the CoinGecko API, archives the raw JSON to AWS S3, and loads it into PostgreSQL.

Transform (T): dbt (Data Build Tool) picks up the raw data, cleans it, tests it, and creates an analytics-ready view (avg_price_analytics).

Visualize: Metabase connects to the transformed data for real-time dashboarding.

## 🛠️ Tech Stack
Orchestration: Apache Airflow (running in Docker)

Transformation: dbt (Data Build Tool) Core

Containerization: Docker & Docker Compose

Language: Python 3.12 (Pandas, Requests, Boto3)

Cloud Storage: AWS S3

Data Warehouse: PostgreSQL

Visualization: Metabase

## 📋 Prerequisites
Before running this project, ensure you have the following installed:

Docker Desktop (running with at least 4GB RAM)

Git

AWS Account (Access Key & Secret Key with S3 write permissions)

## 🚀 Setup & Installation
### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/Crypto-Data-Warehouse-Pipeline.git
cd Crypto-Data-Warehouse-Pipeline
```
### 2. Configure Environment Variables
Create a .env file in the root directory to store your secrets. Note: This file is ignored by Git for security.

```bash
# .env file content
AIRFLOW_UID=50000
AWS_ACCESS_KEY=your_aws_access_key_here
AWS_SECRET_KEY=your_aws_secret_key_here
AWS_BUCKET_NAME=your_s3_bucket_name
```

### 3. Start the Services
Run the following command to build the custom Airflow image (with dbt) and start the stack.

Bash
docker compose up -d --build
Wait 2-3 minutes for the containers to initialize (Airflow, Postgres, Metabase).

### 4. Access the UI
Airflow: http://localhost:8080

User: airflow | Pass: airflow

Metabase: http://localhost:3000

### 5. Configure Airflow Connection
In the Airflow UI, go to Admin → Connections and add:

Plaintext
Conn Id: postgres_dw
Conn Type: Postgres
Host: postgres_dw
Schema: crypto_db
Login: airflow
Password: airflow
Port: 5432
🏃‍♂️ Usage
Activate: Enable the DAG named crypto_etl_pipeline in the Airflow UI.

Schedule: The pipeline runs automatically @hourly.

Manual Trigger: Click the Play Button (▶) to force a run immediately.

## 📊 Verification
Check the Data Warehouse
You can connect to the Postgres database directly or verify via the Airflow logs.

```SQL
-- Check the transformed analytics view created by dbt
SELECT * FROM public.avg_price_analytics 
ORDER BY captured_at DESC 
LIMIT 10;
Visualize in Metabase
Connect Metabase to Host: postgres_dw (Port: 5432).
```
Select the crypto_db database.

Create a chart using the avg_price_analytics table.

```📂 Project Structure
Plaintext
├── dags/
│   └── crypto_pipeline.py    # Main ETL Logic (Airflow DAG)
├── crypto_analytics/         # dbt Project (Transformation Logic)
│   ├── models/               # SQL Models
│   └── dbt_project.yml       # dbt Config
├── docker-compose.yaml       # Container orchestration
├── Dockerfile                # Custom Airflow image with dbt
├── requirements.txt          # Python dependencies
├── README.md                 # Project Documentation
└── .gitignore                # Ignores .env and logs
```