# === Inicialización de paths y sys.path ===
import sys
import os

# === Agregar la raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Imports principales ===
import pandas as pd
from config.path import RAW_CSV_DIR, DASHBOARD_DATA_DIR

# === Configuración de rutas ===
archivo_entrada = RAW_CSV_DIR / 'nvidia_market_analytics.csv'
archivo_salida = DASHBOARD_DATA_DIR / 'csv_procesado.csv'

# === Cargar CSV con encoding seguro ===
try:
    df = pd.read_csv(archivo_entrada, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(archivo_entrada, encoding="latin1")  # Fallback en caso de error de codificación

# === Validación de columnas esperadas ===
expected_cols = [
    "Date", "Product Category", "Product Name", "Region", "Sales Revenue (USD)",
    "Units Sold", "Customer Segment", "Customer Type", "Customer Satisfaction",
    "Marketing Spend (USD)", "Discount Percentage (%)", "Competitor Influence",
    "Return Rate (%)", "AI/ML Adoption Rate (%)", "Ad Campaign Effectiveness",
    "Customer Retention Rate (%)", "Product Launch Date", "Competitor Product", "Market Share (%)"
]

missing = [col for col in expected_cols if col not in df.columns]
if missing:
    raise ValueError(f"Columnas faltantes: {missing}")

# === Conversión de columnas de fecha ===
fecha_cols = ["Date", "Product Launch Date"]
for col in fecha_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# === Conversión de columnas numéricas ===
numericas = [
    "Sales Revenue (USD)", "Units Sold", "Customer Satisfaction",
    "Marketing Spend (USD)", "Discount Percentage (%)", "Return Rate (%)",
    "AI/ML Adoption Rate (%)", "Ad Campaign Effectiveness",
    "Customer Retention Rate (%)", "Market Share (%)"
]

for col in numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# === Limpieza de valores nulos críticos ===
df = df.dropna(subset=["Date", "Product Name", "Sales Revenue (USD)"])

# === Imputación de valores faltantes no críticos ===
df = df.fillna({
    "Customer Satisfaction": df["Customer Satisfaction"].median(),
    "Return Rate (%)": 0.0
})

# === Normalización de texto en columnas categóricas ===
df["Region"] = df["Region"].str.strip().str.title()
df["Customer Type"] = df["Customer Type"].str.strip().str.title()

# === Exportar archivo procesado ===
df.to_csv(archivo_salida, index=False)
print(f"✅ CSV procesado correctamente en: {archivo_salida}")
