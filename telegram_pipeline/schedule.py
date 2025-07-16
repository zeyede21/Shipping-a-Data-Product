from dagster import schedule
from job import full_etl_pipeline

@schedule(cron_schedule="0 9 * * *", job=full_etl_pipeline, execution_timezone="Africa/Addis_Ababa")
def daily_pipeline_schedule(_context):
    return {}
