from databricks.connect import DatabricksSession
import os
from dotenv import load_dotenv

load_dotenv()

def get_spark():
    return DatabricksSession.builder.remote(
        host=os.getenv("databricks_host"),
        token=os.getenv("databricks_token"),
        serverless=True
    ).getOrCreate()
