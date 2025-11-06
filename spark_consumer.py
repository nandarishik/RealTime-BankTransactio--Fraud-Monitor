from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

def process_stream():
    """Connects to Kafka, applies fraud logic, and saves to PostgreSQL."""
    spark = (SparkSession.builder
             .appName("FraudDetection")
             # No longer need to specify packages here, we'll do it in the command
             .getOrCreate())

    spark.sparkContext.setLogLevel("WARN")

    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("merchant", StringType(), True),
        StructField("location_city", StringType(), True),
        StructField("location_state", StringType(), True),
        StructField("is_fraud_actual", IntegerType(), True)
    ])

    kafka_df = (spark.readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", "kafka:29092")
              .option("subscribe", "transactions")
              .option("startingOffsets", "latest")
              .load())

    parsed_df = (kafka_df.selectExpr("CAST(value AS STRING)")
                 .select(from_json(col("value"), schema).alias("data"))
                 .select("data.*"))

    # --- NEW: Add fraud detection logic ---
    # Flag transactions where the amount is greater than 9000
    processed_df = parsed_df.withColumn("is_flagged", when(col("amount") > 9000, 1).otherwise(0))

    # --- NEW: Function to write each batch to PostgreSQL ---
    def write_to_postgres(df, epoch_id):
        print(f"Writing batch {epoch_id} to PostgreSQL...")
        df.write \
          .format("jdbc") \
          .option("url", "jdbc:postgresql://postgres:5432/fraud_detection") \
          .option("dbtable", "transactions") \
          .option("user", "user") \
          .option("password", "password") \
          .option("driver", "org.postgresql.Driver") \
          .mode("append") \
          .save()
        print(f"Batch {epoch_id} written successfully.")

    # --- NEW: Use foreachBatch to write to the database ---
    query = (processed_df.writeStream
             .outputMode("append")
             .foreachBatch(write_to_postgres)
             .start())

    query.awaitTermination()

if __name__ == "__main__":
    process_stream()