import os
import sys

# Signal we're running ON Databricks — session_spark.py uses SparkSession not DatabricksSession
os.environ["ON_DATABRICKS"] = "true"

# Bundle root path so extract can find uploaded data files via spark.read
os.environ["BUNDLE_FILES_ROOT"] = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.etl_pipeline import run_etl_pipeline

run_etl_pipeline()
