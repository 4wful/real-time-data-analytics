# === Inicialización de paths y sys.path ===
import sys
import os

# === Agregar la raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Imports principales ===
import pdfplumber
import pandas as pd
from config.path import RAW_PDF_DIR, DASHBOARD_DATA_DIR
from pathlib import Path
import re

# === Parámetros de configuración ===
pagina_deseada = 0  # Número de página que contiene la tabla
csvs_procesados = []

# === Buscar todos los archivos PDF que comiencen con 'Q' ===
lista_pdfs = sorted([f.name for f in Path(RAW_PDF_DIR).glob("Q*.pdf")])

# === Procesar cada PDF ===
for nombre_pdf in lista_pdfs:
    ruta_pdf = RAW_PDF_DIR / nombre_pdf
    print(f"📄 Procesando: {ruta_pdf}")

    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            pagina = pdf.pages[pagina_deseada]
            tablas = pagina.extract_tables()

        if not tablas:
            print(f"❌ No se encontró ninguna tabla en la página {pagina_deseada + 1}")
            continue

        tabla = tablas[0]
        columnas = tabla[0]
        filas = tabla[1:]

        df = pd.DataFrame(filas, columns=columnas)
        df = df.melt(id_vars=df.columns[0], var_name="Quarter", value_name="Revenue")
        df.columns = ["Business Unit", "Quarter", "Revenue"]

        # Limpiar y normalizar datos
        df["Revenue"] = df["Revenue"].replace(r"[\$,]", "", regex=True).astype(float)
        df["Business Unit"] = df["Business Unit"].str.strip()
        df["Quarter"] = df["Quarter"].str.strip()

        # Agregar metadata del archivo de origen
        df["Source File"] = nombre_pdf

        csvs_procesados.append(df)
        print(f"✅ Datos extraídos correctamente de {nombre_pdf}")

    except Exception as e:
        print(f"❌ Error al procesar {ruta_pdf}: {e}")

# === Guardar resultado final si hubo éxito en al menos un archivo ===
if csvs_procesados:
    df_final = pd.concat(csvs_procesados, ignore_index=True)
    ruta_final = DASHBOARD_DATA_DIR / "pdf_procesado.csv"
    df_final.to_csv(ruta_final, index=False)
    print(f"✅ PDF total procesado guardado como: {ruta_final}")
else:
    print("⚠️ No se generó archivo final: ningún PDF fue procesado exitosamente.")


