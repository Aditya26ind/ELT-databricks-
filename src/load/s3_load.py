from ..utils.logger import get_logger

logger = get_logger(__name__)


def load_to_table(df, table_name: str, mode: str = "overwrite"):
    """Trial: saves to Databricks-managed Unity Catalog table."""
    spark = df.sparkSession
    if spark.catalog.tableExists(table_name):
        df.write.format("delta").mode(mode).saveAsTable(table_name)
    else:
        df.write.format("delta").mode("overwrite").saveAsTable(table_name)
    logger.info(f"Loaded to Unity Catalog table: {table_name}")


def load_to_s3(df, s3_path: str, mode: str = "overwrite"):
    """Production: saves to your own S3 bucket as a Delta table."""
    from delta.tables import DeltaTable
    spark = df.sparkSession
    if DeltaTable.isDeltaTable(spark, s3_path):
        df.write.format("delta").mode(mode).save(s3_path)
    else:
        df.write.format("delta").mode("overwrite").save(s3_path)
    logger.info(f"Loaded to S3 Delta table: {s3_path}")
