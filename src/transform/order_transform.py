from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum, round

from ..utils.logger import get_logger

logger = get_logger(__name__)


def transform_orders(df: DataFrame) -> DataFrame:
    logger.info("Starting transform: dropping nulls, casting, aggregating")

    df = df.dropna(subset=["order_id", "customer_id", "amount"])
    df = df.withColumn("amount", col("amount").cast("double"))

    df_transformed = (
        df.groupBy("customer_id", "product_category")
        .agg(round(sum("amount"), 2).alias("total_spend"))
        .orderBy("customer_id")
    )

    logger.info("Transform complete")
    return df_transformed
