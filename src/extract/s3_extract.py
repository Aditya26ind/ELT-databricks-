import os
import pandas as pd
from pyspark.sql import DataFrame

from ..utils.session_spark import get_spark
from ..utils.logger import get_logger

logger = get_logger(__name__)


def extract_local() -> DataFrame:
    """Trial: reads local CSV and sends to cluster via Databricks Connect."""
    spark = get_spark()
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/sample_orders.csv"))
    logger.info(f"Reading local CSV: {csv_path}")
    return spark.createDataFrame(pd.read_csv(csv_path))


def extract_from_s3() -> DataFrame:
    """Production: reads directly from S3."""
    spark = get_spark()
    s3_path = f"s3a://{os.getenv('S3_BUCKET')}/raw/orders.csv"
    logger.info(f"Reading from S3: {s3_path}")
    return spark.read.format("csv").option("header", "true").load(s3_path)
