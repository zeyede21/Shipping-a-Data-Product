from dagster import job
from ops import scrape_telegram_data, load_raw_to_postgres, run_dbt_transformations, run_yolo_enrichment

@job
def full_etl_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
