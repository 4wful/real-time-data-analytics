import sys
import os

# === Agregar la raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Cargar variables del .env manualmente desde la raíz ===
env_path = os.path.join(ROOT_DIR, '.env')

if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
else:
    raise FileNotFoundError(f"No se encontró el archivo .env en: {env_path}")

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")

# === Spark y procesamiento ===
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
from config.path import ML_TRAINING_DATA_DIR, CHECKPOINT_ML_DIR

spark = SparkSession.builder \
    .appName("KafkaSparkETL_ML") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5") \
    .config("spark.sql.shuffle.partitions", "3") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("symbol", StringType()) \
    .add("timestamp", StringType()) \
    .add("open", StringType()) \
    .add("high", StringType()) \
    .add("low", StringType()) \
    .add("close", StringType()) \
    .add("volume", StringType())

df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

df_ml = df_parsed.select("open", "high", "low", "close", "volume")

query_ml = df_ml.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", str(ML_TRAINING_DATA_DIR)) \
    .option("checkpointLocation", str(CHECKPOINT_ML_DIR)) \
    .start()

query_ml.awaitTermination()




