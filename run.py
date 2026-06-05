import os
import sys

# Signal we're running ON Databricks — session_spark.py uses SparkSession not DatabricksSession
os.environ["ON_DATABRICKS"] = "true"

# Databricks serverless runs this file via exec(compile(...)) which may not define __file__.
# Fall back to cwd, which is the bundle files root in that execution context.
try:
    _bundle_root = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _bundle_root = os.getcwd()

os.environ["BUNDLE_FILES_ROOT"] = _bundle_root
sys.path.insert(0, _bundle_root)

from src.etl_pipeline import run_etl_pipeline

run_etl_pipeline()
