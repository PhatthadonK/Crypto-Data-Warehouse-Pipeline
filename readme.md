# 📈 The Crypto Market Data Warehouse

A robust, containerized ETL (Extract, Transform, Load) pipeline that ingests real-time cryptocurrency market data, stores raw history in a Data Lake (AWS S3), and loads clean analytics-ready data into a Data Warehouse (PostgreSQL).

## 🏗️ Architecture

**Flow:** `CoinGecko API` → `Airflow (Extract)` → `AWS S3 (Raw Storage)` → `Airflow (Transform via Pandas)` → `PostgreSQL (Data Warehouse)`



The pipeline consists of two major stages:
1.  **Bronze Layer (Extract):** Fetches live market data (Price, Volume, Rank) from the CoinGecko API and saves the raw JSON into an AWS S3 Bucket.
2.  **Silver/Gold Layer (Transform & Load):** Downloads the raw JSON from S3, cleans/formats the data using Pandas, and loads it into a Postgres Data Warehouse for analysis.

## 🛠️ Tech Stack

* **Orchestration:** Apache Airflow (running in Docker)
* **Containerization:** Docker & Docker Compose
* **Language:** Python 3.12 (Pandas, Requests, Boto3)
* **Cloud Storage:** AWS S3
* **Data Warehouse:** PostgreSQL
* **Source:** CoinGecko Public API

## 📋 Prerequisites

Before running this project, ensure you have the following installed:
* **Docker Desktop** (running with at least 4GB RAM)
* **Git**
* **AWS Account** (Access Key & Secret Key with S3 write permissions)

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Crypto-Data-Warehouse-Pipeline.git](https://github.com/YourUsername/Crypto-Data-Warehouse-Pipeline.git)
cd Crypto-Data-Warehouse-Pipeline
```

### 2. Configure Environment Variables
Create a .env file in the root directory to store your secrets. Note: This file is ignored by Git for security.

```bash
# .env file content
AIRFLOW_UID=50000
AWS_ACCESS_KEY=your_aws_access_key_here
AWS_SECRET_KEY=your_aws_secret_key_here
```

### 3. Start the Services
Run the following command to initialize Airflow and the Database.

```bash
docker compose up -d
Wait 2-3 minutes for the containers to initialize (Airflow Webserver, Scheduler, Postgres, Redis).
```

### 4. Access Airflow
Open your browser and go to: http://localhost:8080

Username: airflow

Password: airflow

### 5. Configure the Database Connection
In Airflow UI, go to Admin -> Connections.

Add a new connection:

Conn Id: postgres_dw

Conn Type: Postgres

Host: postgres_dw

Schema: crypto_db

Login: airflow

Password: airflow

Port: 5432

🏃‍♂️ Usage
Enable the DAG named crypto_etl_pipeline in the Airflow UI.

The pipeline runs automatically @hourly.

To trigger a manual run, click the Play Button (▶).

Verification
You can check the data in the Postgres Warehouse by connecting to the database:

SQL
SELECT * FROM crypto_prices ORDER BY captured_at DESC LIMIT 10;
📂 Project Structure
Plaintext
├── dags/
│   └── crypto_pipeline.py   # Main ETL Logic (Airflow DAG)
├── docker-compose.yaml      # Container orchestration
├── requirements.txt         # Python dependencies
├── README.md                # Project Documentation
└── .gitignore               # Ignores .env and logs