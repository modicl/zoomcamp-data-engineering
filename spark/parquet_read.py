from pyspark.sql import SparkSession
from pathlib import Path

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("parquet-read") \
    .config("spark.driver.memory", "16g") \
    .getOrCreate()


RELATIVE_PATH = Path(__file__).parent / "data" / "yellow_tripdata_2025-12.parquet"

df = spark.read.parquet(str(RELATIVE_PATH))

df.printSchema()

select_basico = df.select('payment_type' , 'fare_amount' , 'extra').filter(df.payment_type == 0)
select_basico.show(5)