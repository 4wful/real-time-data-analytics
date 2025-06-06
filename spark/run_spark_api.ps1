# --- [1] Configurar entorno Spark ---
$env:PYSPARK_PYTHON = "C:\Users\Guido Maidana\AppData\Local\Programs\Python\Python312\python.exe"
$env:PYSPARK_DRIVER_PYTHON = "C:\Users\Guido Maidana\AppData\Local\Programs\Python\Python312\python.exe"

# --- [2] Ejecutar Spark ETL con Kafka para ML ---
Write-Host "`n▶ Iniciando proceso Spark Kafka ETL para ML..."
Start-Process -NoNewWindow -FilePath "spark-submit" -ArgumentList "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 spark_api.py"


Write-Host "✅ Procesamiento estático completado con éxito."


