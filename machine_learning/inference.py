import sys
import os

# === Agregar la raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Imports ===
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from config.path import (
    ML_CSV_PATH,
    BEST_MODEL_PATH,
    BEST_FEATURES_PATH,
    PRED_CSV_PATH
)

# === Cargar dataset original ===
df = pd.read_csv(ML_CSV_PATH)
df = df.dropna().astype(float)

# === Cargar modelo y features ===
modelo = joblib.load(BEST_MODEL_PATH)
with open(BEST_FEATURES_PATH, 'r') as f:
    features = f.read().strip().split(',')

X = df[features]
y = df['close']

# === Realizar predicciones ===
predicciones = modelo.predict(X)

# === Evaluar rendimiento ===
mse = mean_squared_error(y, predicciones)
r2 = r2_score(y, predicciones)

print(f"📊 MSE: {mse:.4f}")
print(f"📈 R²: {r2:.4f}")

# === Guardar resultados ===
df_resultado = pd.DataFrame({
    'real': y,
    'predicho': predicciones
})
df_resultado.to_csv(PRED_CSV_PATH, index=False)
print(f"✅ Archivo de predicciones guardado en: {PRED_CSV_PATH}")

# === Visualización ===
plt.figure(figsize=(10, 5))
plt.plot(df_resultado['real'].values[:100], label='Real', marker='o')
plt.plot(df_resultado['predicho'].values[:100], label='Predicho', marker='x')
plt.title('Comparación: Precio de cierre real vs predicho')
plt.xlabel('Muestras')
plt.ylabel('Precio de cierre')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


