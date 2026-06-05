# Orchestration

This folder contains examples and guidance for running the pipeline as a Databricks job.

## Databricks Job

In Databricks, create a job that runs a notebook or Python script.

### Example task
- Task type: Notebook or Python script
- Notebook path: `/Workspace/Users/you@example.com/elt_pipeline`
- Parameters:
  - `raw_path`: `s3a://your-bucket/raw/orders_raw.csv`
  - `staging_path`: `s3a://your-bucket/staging/orders_delta`
  - `output_path`: `s3a://your-bucket/output/orders_summary`

## External orchestration

Use Airflow, Prefect, or a shell script to trigger the Databricks job or to run the pipeline locally.
