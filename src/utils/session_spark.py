import os
from dotenv import load_dotenv

load_dotenv()

_spark = None


def get_spark():
    global _spark
    if _spark is not None:
        return _spark

    # ON_DATABRICKS set by run.py (serverless jobs don't set DATABRICKS_RUNTIME_VERSION)
    # DATABRICKS_RUNTIME_VERSION set by classic clusters
    if os.getenv("ON_DATABRICKS") or os.getenv("DATABRICKS_RUNTIME_VERSION"):
        from pyspark.sql import SparkSession
        _spark = SparkSession.builder.getOrCreate()
    else:
        from databricks.connect import DatabricksSession
        _spark = DatabricksSession.builder.remote(
            host=os.getenv("databricks_host"),
            token=os.getenv("databricks_token"),
            serverless=True,
        ).getOrCreate()

    return _spark
