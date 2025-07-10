import sys
import os
import shutil
from pyspark.sql import SparkSession

# === Agregar raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from config.path import (
    ML_TRAINING_DATA_DIR,
    ML_CSV_TEMP_PATH,
    ML_CSV_FINAL_PATH,
    ML_ZIP_FINAL_PATH
)

spark = SparkSession.builder \
    .appName("ParquetToCSV_MLOnly") \
    .master("local[*]") \
    .getOrCreate()

def parquet_to_csv_zip(parquet_path, csv_temp_path, csv_final_path, zip_final_path):
    df = spark.read.parquet(str(parquet_path))

    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(str(csv_temp_path))

    # Buscar CSV real generado
    csv_files = [f for f in os.listdir(csv_temp_path) if f.endswith(".csv")]
    if not csv_files:
        raise Exception(f"❌ No se encontró archivo CSV en: {csv_temp_path}")
    csv_file_path = os.path.join(csv_temp_path, csv_files[0])

    # Limpiar y mover CSV al destino final
    if os.path.exists(csv_final_path):
        os.remove(csv_final_path)
    os.rename(csv_file_path, csv_final_path)
    shutil.rmtree(csv_temp_path)

    shutil.make_archive(csv_final_path.with_suffix(''), 'zip',
                        root_dir=os.path.dirname(csv_final_path),
                        base_dir=os.path.basename(csv_final_path))

    print(f"✅ CSV generado en: {csv_final_path}")
    print(f"✅ ZIP generado en: {zip_final_path}")

if __name__ == "__main__":
    parquet_to_csv_zip(
        ML_TRAINING_DATA_DIR,
        ML_CSV_TEMP_PATH,
        ML_CSV_FINAL_PATH,
        ML_ZIP_FINAL_PATH
    )
    