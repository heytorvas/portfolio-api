from enum import Enum


class SkillEnum(str, Enum):
    """Enum for technical skills."""

    PYTHON = "Python"
    FASTAPI = "FastAPI"
    MONGODB = "MongoDB"
    POSTGRESQL = "PostgreSQL"
    DOCKER = "Docker"
    KUBERNETES = "Kubernetes"
    AIRFLOW = "Airflow"
    SPARK = "Spark"
    GCS = "GCS"
    AWS = "AWS"
    BIGQUERY = "BigQuery"
    DATABRICKS = "Databricks"
    SCRUM = "Scrum"
    KANBAN = "Kanban"
