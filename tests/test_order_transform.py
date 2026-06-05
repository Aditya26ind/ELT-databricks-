from pyspark.sql import Row
from src.transform.order_transform import transform_orders


def test_aggregates_spend_per_customer_category(spark):
    data = [
        Row(order_id="1", customer_id="200", order_date="2026-01-01", amount="100.00", product_category="electronics"),
        Row(order_id="2", customer_id="200", order_date="2026-01-02", amount="50.00",  product_category="electronics"),
        Row(order_id="3", customer_id="201", order_date="2026-01-03", amount="75.00",  product_category="grocery"),
    ]
    df = spark.createDataFrame(data)
    result = transform_orders(df)
    rows = {(r.customer_id, r.product_category): r.total_spend for r in result.collect()}

    assert rows[("200", "electronics")] == 150.0
    assert rows[("201", "grocery")] == 75.0


def test_drops_rows_with_null_amount(spark):
    data = [
        Row(order_id="1", customer_id="200", order_date="2026-01-01", amount=None,    product_category="electronics"),
        Row(order_id="2", customer_id="201", order_date="2026-01-02", amount="50.00", product_category="grocery"),
    ]
    df = spark.createDataFrame(data)
    result = transform_orders(df)

    assert result.count() == 1
    assert result.collect()[0].customer_id == "201"


def test_drops_rows_with_null_customer_id(spark):
    data = [
        Row(order_id="1", customer_id=None,  order_date="2026-01-01", amount="100.00", product_category="electronics"),
        Row(order_id="2", customer_id="201", order_date="2026-01-02", amount="50.00",  product_category="grocery"),
    ]
    df = spark.createDataFrame(data)
    result = transform_orders(df)

    assert result.count() == 1


def test_output_schema_has_expected_columns(spark):
    data = [
        Row(order_id="1", customer_id="200", order_date="2026-01-01", amount="100.00", product_category="electronics"),
    ]
    df = spark.createDataFrame(data)
    result = transform_orders(df)

    assert set(result.columns) == {"customer_id", "product_category", "total_spend"}


def test_empty_dataframe_returns_empty(spark):
    data = []
    schema = "order_id string, customer_id string, order_date string, amount string, product_category string"
    df = spark.createDataFrame(data, schema)
    result = transform_orders(df)

    assert result.count() == 0
