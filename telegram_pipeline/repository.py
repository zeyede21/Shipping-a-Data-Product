# telegram_pipeline/repository.py

from dagster import Definitions
from telegram_pipeline .job import full_etl_pipeline

defs = Definitions(
    jobs=[full_etl_pipeline]
)
