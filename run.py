import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.etl_pipeline import run_etl_pipeline

if __name__ == "__main__":
    run_etl_pipeline()
