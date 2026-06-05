import pytest
from src.utils.session_spark import get_spark


@pytest.fixture(scope="session")
def spark():
    # Uses Databricks Connect — tests run on the remote serverless cluster
    return get_spark()
