import os
from dotenv import load_dotenv

from .utils.session_spark import get_spark
from .utils.logger import get_logger
from .extract.s3_extract import extract_local, extract_from_s3
from .transform.order_transform import transform_orders
from .load.s3_load import load_to_table, load_to_s3

load_dotenv()
logger = get_logger(__name__)

PRODUCTION = os.getenv("PRODUCTION", "false").lower() == "true"

BRONZE_TABLE = "workspace.default.orders_bronze"
SILVER_TABLE = "workspace.default.orders_silver"

S3_BUCKET    = os.getenv("S3_BUCKET", "your-bucket")
BRONZE_PATH  = f"s3a://{S3_BUCKET}/bronze/orders"
SILVER_PATH  = f"s3a://{S3_BUCKET}/silver/orders_summary"


def run_etl_pipeline():
    spark = get_spark()
    logger.info(f"Pipeline started — mode: {'PRODUCTION' if PRODUCTION else 'TRIAL'}")

    if PRODUCTION:
        raw_df    = extract_from_s3()
        load_to_s3(raw_df, BRONZE_PATH)
        bronze_df = spark.read.format("delta").load(BRONZE_PATH)
    else:
        spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.default")
        raw_df    = extract_local()
        load_to_table(raw_df, BRONZE_TABLE)
        bronze_df = spark.table(BRONZE_TABLE)

    transformed_df = transform_orders(bronze_df)

    if PRODUCTION:
        load_to_s3(transformed_df, SILVER_PATH)
    else:
        load_to_table(transformed_df, SILVER_TABLE)

    logger.info("Pipeline complete")


if __name__ == "__main__":
    run_etl_pipeline()
