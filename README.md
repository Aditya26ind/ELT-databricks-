# Databricks ELT Study Project

This repository contains a simple end-to-end ELT study project for Databricks using Python, Spark, and S3.

## Structure

- `src/` - Python pipeline code
  - `extract/` - extract raw data from S3
  - `transform/` - clean and aggregate data
  - `load/` - write results back to S3 / Delta
- `orch/` - orchestration and job guidance
- `tests/` - unit tests for the pipeline
- `configs/` - optional configuration examples for S3 paths and environments
- `notebooks/` - optional Databricks notebook examples and walkthroughs
- `data/` - sample input data for local development

## How to use

1. Upload a sample raw CSV to S3.
2. Update the S3 paths in `src/etl_pipeline.py` or pass them with the CLI.
3. Run with Spark locally for development, or move the functions into a Databricks notebook.
4. Use `orch/databricks_job_spec.json` or `orch/orchestrator.py` as a pattern for job orchestration.

## Local development

Install requirements:

```bash
pip install -r requirements.txt
```

Run the pipeline locally:

```bash
python src/etl_pipeline.py           --raw-path s3a://your-bucket/raw/orders_raw.csv           --staging-path s3a://your-bucket/staging/orders_delta           --output-path s3a://your-bucket/output/orders_summary
```

> On Databricks, you can import `src.extract.s3_extract`, `src.transform.order_transform`, and `src.load.s3_load` directly in a notebook and use the existing `spark` session.
