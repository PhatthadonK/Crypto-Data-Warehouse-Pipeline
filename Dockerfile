FROM apache/airflow:2.10.2

USER root
RUN apt-get update && apt-get install -y git

USER airflow
RUN pip install --no-cache-dir dbt-postgres