import sys
import os

# === Setup de paths ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Imports ===
import pandas as pd
import numpy as np
import joblib
from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from config.path import ML_CSV_PATH, BEST_MODEL_PATH, BEST_FEATURES_PATH

# === Cargar dataset ===
df = pd.read_csv(ML_CSV_PATH)

# === Limpiar y seleccionar solo columnas numéricas ===
columnas_numericas = ['open', 'high', 'low', 'close', 'volume']
df = df.dropna(subset=columnas_numericas)
df = df[columnas_numericas].astype(float)

print(f"📦 Total de registros válidos: {len(df)}")
print(df.describe())

# === Función de entrenamiento y evaluación ===
def entrenar_modelo(X_train, y_train, X_test, y_test, modelo, nombre):
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{nombre} → 📊 MSE: {mse:.4f} | 📈 R²: {r2:.4f}")
    return modelo, mse, r2

# === Probar todas las combinaciones de features ===
features_totales = ['open', 'high', 'low', 'volume']
combinaciones = [list(c) for r in range(1, len(features_totales) + 1) for c in combinations(features_totales, r)]

# === Entrenamiento ===
mejor_r2 = -np.inf
mejor_modelo = None
mejores_features = []
mejor_tipo = ""

for features in combinaciones:
    try:
        X = df[features]
        y = df['close']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        # Entrenar ambos modelos
        modelos = {
            "LinearRegression": LinearRegression(),
            "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42)
        }

        for nombre, modelo in modelos.items():
            modelo_entrenado, mse, r2 = entrenar_modelo(X_train, y_train, X_test, y_test, modelo, nombre)
            if r2 > mejor_r2:
                mejor_r2 = r2
                mejor_modelo = modelo_entrenado
                mejores_features = features
                mejor_tipo = nombre
                joblib.dump(mejor_modelo, BEST_MODEL_PATH)
                with open(BEST_FEATURES_PATH, 'w') as f:
                    f.write(','.join(features))
                print(f"💾 ¡Nuevo mejor modelo guardado! ({nombre})")
    except Exception as e:
        print(f"⚠️ Error con features {features}: {e}")

print("\n✅ Entrenamiento completo.")
print(f"🏆 Mejor R²: {mejor_r2:.4f} con modelo: {mejor_tipo} y features: {mejores_features}")
