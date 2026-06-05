import os
from dotenv import load_dotenv

load_dotenv()


def get_spark():
    if os.getenv("DATABRICKS_RUNTIME_VERSION"):
        from pyspark.sql import SparkSession
        return SparkSession.builder.getOrCreate()

    from databricks.connect import DatabricksSession
    return DatabricksSession.builder.remote(
        host=os.getenv("databricks_host"),
        token=os.getenv("databricks_token"),
        serverless=True,
    ).getOrCreate()
