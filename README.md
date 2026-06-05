# Databricks ELT Pipeline

End-to-end ELT pipeline built with Python, PySpark, and Databricks Connect. Reads raw CSV data, loads it to Delta tables, transforms it, and saves the result — following the Bronze/Silver Medallion architecture.

---

## Project Structure

```
DatabrikcsELT/
├── src/
│   ├── extract/          # Read raw data (local CSV or S3)
│   ├── transform/        # Clean and aggregate with PySpark
│   ├── load/             # Write to Delta (Unity Catalog or S3)
│   └── utils/
│       ├── session_spark.py   # Databricks Connect session
│       └── logger.py          # Shared logging setup
├── tests/                # Pytest tests (run against Databricks cluster)
├── data/                 # Sample CSV for local/trial development
├── configs/              # Example path configs
├── orch/                 # Orchestration notes
├── .env                  # Credentials (never committed)
└── requirements.txt
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create `.env` in the project root
```
databricks_host=https://your-workspace.azuredatabricks.net
databricks_token=dapi...

# Production only
PRODUCTION=false
S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

### 3. Get Databricks credentials
| Value | Where to find it |
|---|---|
| `databricks_host` | Browser URL when on your Databricks workspace |
| `databricks_token` | Settings → Developer → Access Tokens → Generate |

---

## Running the Pipeline

```bash
python -m src.etl_pipeline
```

### Trial mode (`PRODUCTION=false`)
- Reads from `data/sample_orders.csv` locally
- Writes to `workspace.default.orders_bronze` and `workspace.default.orders_silver` in Unity Catalog
- No S3 credentials needed

### Production mode (`PRODUCTION=true`)
- Reads from `s3a://<S3_BUCKET>/raw/orders.csv`
- Writes Delta tables to your own S3 bucket
- Requires AWS credentials and External Location configured in Unity Catalog

---

## ELT Flow

```
CSV (local or S3)
      ↓  Extract
DataFrame (Databricks cluster memory)
      ↓  Load
Bronze Delta Table  ← raw data persisted
      ↓  Read back
      ↓  Transform (clean, aggregate)
Silver Delta Table  ← final output
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests run against the real Databricks serverless cluster — credentials in `.env` must be set.

---

## Architecture Notes

- **Databricks Connect** — code runs locally, executes on a remote Databricks serverless cluster
- **Delta Lake** — all tables use Delta format for ACID transactions and time travel
- **Unity Catalog** — trial uses Databricks-managed storage; production uses your own S3 via External Location
- **Medallion layers** — Bronze (raw) → Silver (cleaned/aggregated)
