# 1. Infrastructure Requirements
Instance: AWS EC2 (Ubuntu 24.04 or 22.04)

Size: t3.medium (Recommended) or t2.medium (Minimum 4GB RAM).

Security Group (Inbound Rules):

SSH (22) -> My IP

Custom TCP (8080) -> Anywhere (0.0.0.0/0) - For Airflow

Custom TCP (3000) -> Anywhere (0.0.0.0/0) - For Metabase

# 2. The File Directory Structure
This is exactly how your folder (~/Crypto-Data-Warehouse-Pipeline) must look for the Docker mount to work.

Plaintext
Crypto-Data-Warehouse-Pipeline/      <-- Project Root
├── dags/                            <-- Python Pipeline scripts (chmod 777)
├── logs/                            <-- Airflow Logs (chmod 777)
├── plugins/                         <-- Custom plugins (chmod 777)
├── dbt/                             <-- dbt project files (chmod 777)
├── crypto_analytics/                <-- dbt models (chmod 777)
├── .env                             <-- Passwords & Keys (Created manually)
├── docker-compose.yaml              <-- The main blueprint
├── docker-compose.override.yaml     <-- The "Performance Patch"
├── Dockerfile                       <-- Custom image instructions
└── requirements.txt                 <-- Python libraries (chmod 777)
# 3. Setup & Permissions Commands (The Script)
Run these commands in order on a fresh EC2 instance.

## Phase A: Install Engine (Docker)
```bash
# Update and install Docker
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker components
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Allow 'ubuntu' user to run Docker (No sudo needed later)
sudo usermod -aG docker $USER
newgrp docker
```

## Phase B: Project Setup & Permissions (Crucial)
```Bash
# 1. Clone the Repo
git clone https://github.com/PhatthadonK/Crypto-Data-Warehouse-Pipeline.git
cd Crypto-Data-Warehouse-Pipeline

# 2. Create Missing Folders
mkdir -p ./dags ./logs ./plugins ./dbt

# 3. Create the "Dummy" Requirements file (Prevents Crash Loop)
touch requirements.txt

# 4. SET PERMISSIONS (The Magic Step)
# This prevents "Permission Denied" errors when Airflow tries to write logs or dbt profiles.
sudo chmod -R 777 dags logs plugins dbt requirements.txt
```
## Phase C: Configuration Files
You must manually create these two files.

### 1. The Secrets (.env) nano .env

```Bash
AIRFLOW_UID=1000
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=crypto_db
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```
### 2. The Performance Patch (docker-compose.override.yaml) nano docker-compose.override.yaml

```bash
services:
  airflow-webserver:
    environment:
      AIRFLOW__WEBSERVER__WORKER_CLASS: gevent
      AIRFLOW__WEBSERVER__WORKERS: 4
      AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT: 120
```
# 4. How to Run & Stop
Start the Server:

```Bash
docker compose up -d
Check Health:
```
```Bash
docker compose ps
docker stats --no-stream
Create Login User (Run once):
```
```Bash
docker compose exec airflow-webserver airflow users create \
    --username airflow \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password airflow
```
Stop the Server (Safe Shutdown):

```Bash
docker compose down
```
Nuke Everything (Factory Reset):

```Bash
docker compose down -v
docker system prune -a --volumes
```
# 5. Accessing the Project
Airflow UI: http://YOUR_PUBLIC_IP:8080

Metabase UI: http://YOUR_PUBLIC_IP:3000