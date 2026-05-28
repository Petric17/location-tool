from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'petric17',
    'depends_on_past': False,
    'email_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'generate_location_map',
    default_args=default_args,
    description='Trigger my Geospatial Docker Tool',
    schedule=None,
    start_date=datetime(2026, 5, 28),
    catchup=False
) as dag:
    run_mapping_container = DockerOperator(
        task_id='run_geospatial_tool',
        image='ghcr.io/petric17/location-tool:latest',
        container_name='airflow_map_task',
        docker_url="tcp://host.docker.internal:2375", 
        auto_remove='success',
        api_version='auto',
        user='root'
    )
    