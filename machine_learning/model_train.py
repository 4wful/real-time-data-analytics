import sys
import os

# === Agregar la raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Imports ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from itertools import combinations

# === Cargar dataset ===
ruta_csv = '../output/ml_training_data/ml_training_data.csv'
df = pd.read_csv(ruta_csv)
print("✅ Dataset cargado correctamente.")

# === Limpieza básica ===
df = df.dropna().astype(float)

# === Análisis exploratorio ===
print(df.describe())
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Matriz de correlación')
plt.show()

# === Función de entrenamiento y evaluación ===
def entrenar_y_evaluar_modelo(features, test_size=0.2):
    print(f"\n🔎 Usando features: {features} | test_size={test_size}")

    X = df[features]
    y = df['close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("📊 MSE:", mse)
    print("📈 R²:", r2)

    if len(features) == 1:
        plt.figure(figsize=(8, 5))
        plt.scatter(X_test, y_test, color='blue', label='Real')
        plt.plot(X_test, y_pred, color='red', label='Predicción')
        plt.xlabel(features[0])
        plt.ylabel('close')
        plt.title(f'Regresión lineal simple: {features[0]} vs close')
        plt.legend()
        plt.show()

    return modelo, mse, r2

# === Generar combinaciones de features ===
features_totales = ['open', 'high', 'low', 'volume']
combinaciones = [list(c) for r in range(1, len(features_totales) + 1) for c in combinations(features_totales, r)]

# === Entrenamiento y búsqueda del mejor modelo ===
mejor_r2 = -np.inf
mejor_modelo = None
mejores_features = []

for features in combinaciones:
    modelo, mse, r2 = entrenar_y_evaluar_modelo(features, test_size=0.1)
    if r2 > mejor_r2:
        mejor_r2 = r2
        mejor_modelo = modelo
        mejores_features = features
        joblib.dump(modelo, 'modelo_final.pkl')
        with open('mejores_features.txt', 'w') as f:
            f.write(','.join(features))
        print("💾 ¡Nuevo mejor modelo guardado!")

print("\n✅ Entrenamiento completo.")
print(f"🏆 Mejor R²: {mejor_r2:.4f} con features: {mejores_features}")