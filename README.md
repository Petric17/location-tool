Location Tool & Orchestrator  
This repository contains a geospatial mapping tool and an Airflow-based orchestration system to automate the generation of location maps.

Project Structure:
/scripts: Core Python logic for geospatial data processing and map generation.
/airflow-orchestrator: Docker-compose setup for Apache Airflow 3.x.
/dags: Contains my_mapping_dag.py which schedules and triggers the tool.
/Maps: Output directory where generated .html or .png maps are stored.

Start the Orchestrator:
cd airflow-orchestrator
docker compose up -d
Access Airflow: Open http://localhost:8080.
Trigger: Unpause the generate_location_map DAG and hit Play.

Technology Stack:
Engine: Python (GeoPandas, Folium)
Orchestration: Apache Airflow
Deployment: Docker & GitHub Actions (GHCR)

