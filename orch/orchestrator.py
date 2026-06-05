import os
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

load_dotenv()

JOB_NAME = "ELT Pipeline - Orders"


def trigger_pipeline():
    client = WorkspaceClient(
        host=os.getenv("databricks_host"),
        token=os.getenv("databricks_token"),
    )
    jobs = list(client.jobs.list(name=JOB_NAME))
    if not jobs:
        raise ValueError(f"Job '{JOB_NAME}' not found — deploy the bundle first")
    run = client.jobs.run_now(job_id=jobs[0].job_id)
    print(f"Triggered run ID: {run.run_id}")
    return run.run_id


if __name__ == "__main__":
    trigger_pipeline()
