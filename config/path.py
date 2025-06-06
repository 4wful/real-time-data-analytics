# === config/path.py ===
from pathlib import Path

# === Base del proyecto ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Carpetas de datos crudos ===
RAW_DATA_DIR = BASE_DIR / 'raw_data'
RAW_CSV_DIR = RAW_DATA_DIR / 'csv'
RAW_PDF_DIR = RAW_DATA_DIR / 'pdf'

# === Carpetas de salida ===
OUTPUT_DIR = BASE_DIR / 'output'

DASHBOARD_DATA_DIR = OUTPUT_DIR / 'dashboard_data'        
ML_TRAINING_DATA_DIR = OUTPUT_DIR / 'ml_training_data'    
PREDICTIONS_DIR = OUTPUT_DIR / 'predictions'               
CHECKPOINTS_DIR = OUTPUT_DIR / 'checkpoints'
CHECKPOINT_ML_DIR = CHECKPOINTS_DIR / 'ml_training'        

# === Rutas para parquet_to_csv.py ===
ML_CSV_TEMP_PATH = ML_TRAINING_DATA_DIR / 'csv_temp'
ML_CSV_FINAL_PATH = ML_TRAINING_DATA_DIR / 'ml_training_data.csv'
ML_ZIP_FINAL_PATH = ML_TRAINING_DATA_DIR / 'ml_training_data.zip'

# === Rutas para scripts de entrenamiento y predicción ===
ML_CSV_PATH = ML_TRAINING_DATA_DIR / 'ml_training_data.csv'
BEST_MODEL_PATH = BASE_DIR / 'machine_learning' / 'modelo_final.pkl'
BEST_FEATURES_PATH = BASE_DIR / 'machine_learning' / 'mejores_features.txt'
PRED_CSV_PATH = PREDICTIONS_DIR / 'predicciones_vs_reales.csv'

# === Rutas para archivos procesados estáticos ===
CSV_PROCESADO_PATH = DASHBOARD_DATA_DIR / 'csv_procesado.csv'
PDF_PROCESADO_PATH = DASHBOARD_DATA_DIR / 'pdf_procesado.csv'

# === Scripts y herramientas ===
STATIC_ETL_DIR = BASE_DIR / 'static_etl'
SPARK_DIR = BASE_DIR / 'spark'
UTILS_DIR = BASE_DIR / 'utils'
KAFKA_DIR = BASE_DIR / 'kafka'

# === Archivos individuales ===
DOCKER_COMPOSE_FILE = KAFKA_DIR / 'docker-compose.yml'
POWER_BI_FILE = BASE_DIR / 'power_bi' / 'nvidia_dashboard.pbix'

# === Notas de uso ===
# Puedes importar cualquier ruta en tus scripts:

#import sys
#import os

# === Agregar la raíz del proyecto al sys.path ===
#CURRENT_DIR = os.path.dirname(__file__)
#ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
#if ROOT_DIR not in sys.path:
    #sys.path.append(ROOT_DIR)

    
# from config.path import RAW_CSV_DIR, ML_CSV_FINAL_PATH, CSV_PROCESADO_PATH, etc.


