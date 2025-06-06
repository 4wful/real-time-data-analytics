# --- [1] Configurar entorno Spark ---
$env:PYSPARK_PYTHON = "C:\Users\Guido Maidana\AppData\Local\Programs\Python\Python312\python.exe"
$env:PYSPARK_DRIVER_PYTHON = "C:\Users\Guido Maidana\AppData\Local\Programs\Python\Python312\python.exe"

# --- [2] Ejecutar conversión de Parquet a CSV ---
Write-Host "`n▶ Iniciando conversión de archivos Parquet a CSV..."
python parquet_to_csv.py

Write-Host "`n✅ Conversión completada correctamente."


