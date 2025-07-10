# 📊 Proyecto: Predicción Financiera para NVIDIA en Tiempo Real
Este repositorio contiene un sistema completo de análisis y predicción financiera enfocado en la empresa NVIDIA, utilizando técnicas de Machine Learning como regresión lineal y Random Forest para realizar predicciones en tiempo real.

El sistema procesa datos bursátiles en vivo mediante Apache Kafka y Apache Spark, entrena modelos con Spark ML y Python, y visualiza los resultados a través de dashboards en Power BI para facilitar decisiones estratégicas.

🔧 Actualmente optimizado para ejecutarse en un entorno WSL2 + Ubuntu, mejorando el rendimiento, escalabilidad y manejo de recursos en entornos Linux.

---

## 🛠️ Tecnologías utilizadas

- **Apache Kafka**: Streaming de datos financieros en tiempo real  
- **Apache Spark**: Procesamiento ETL distribuido y streaming  
- **Python**: Procesamiento de datos y modelos de ML  
- **Power BI**: Visualización de insights y KPIs financieros  
- **Docker**: Contenedores para Kafka y Zookeeper  
- **WSL2 + Ubuntu**: Entorno de desarrollo Linux para alto rendimiento

---

## 📁 Estructura general del proyecto

```
├── config/ # Configuración central (paths, constantes)
├── kafka_services/ # Docker Compose para Kafka y Zookeeper
├── machine_learning/ # Entrenamiento y predicción ML
├── output/ # Archivos finales CSV, gráficos, modelos
├── producer/ # API → Kafka (streaming)
├── raw_data/ # CSV y PDF crudos
├── spark/ # Lógica de Spark Streaming
├── static_etl/ # ETL estático (CSV/PDF)
├── utils/ # Scripts auxiliares
├── .env # Variables sensibles (no incluido en Git)
├── .gitignore # Archivos y carpetas excluidos
├── run_after_streaming.sh # Script automatizado del flujo completo
├── requirements.txt # Dependencias del proyecto
└── README.md # Documentación general
```

## 🧰 Requisitos del sistema

Instala los siguientes componentes antes de ejecutar el proyecto:

- Ubuntu + WSL2 
- Python 3.10 
- Java JDK 11 
- Apache Spark  
- Apache Hadoop 
- Docker Desktop  
- Power BI Desktop  
---

## 🚀 Pasos para ejecutar el proyecto

### 1. Clonar y preparar entorno

```bash
git clone https://github.com/4wful/real-time-data-analytics.git
cd real-time-data-analytics
python -m venv venv
source venv/bin/activate      # En Linux o WSL2
pip install -r requirements.txt
```

### 2. Configurar archivo

🔐 Este archivo no se sube al repositorio por seguridad.

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
API_KEY=tu_api_key_de_alpha_vantage
KAFKA_TOPIC=nombre_topic
KAFKA_BOOTSTRAP_SERVERS=localhost:9092,localhost:9093,localhost:9094
DEST_WIN_PATH=/mnt/c/Users/TU_USUARIO/Desktop/.../BusinessAnalytics/data
```

### 3. Levantar servicios Kafka

```bash
cd kafka_services
docker-compose up -d
```

Crear y verificar el tópico:

```bash
# Crear tópico
docker exec -it kafka-broker-1 kafka-topics --create \
  --bootstrap-server kafka-broker-1:29092 \
  --replication-factor 3 --partitions 3 \
  --topic nombre_topic --if-not-exists

# Listar tópicos existentes
docker exec -it kafka-broker-1 kafka-topics --list \
  --bootstrap-server kafka-broker-1:29092
```

### 4. Ejecutar el flujo de datos

```bash
cd spark
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 spark_api.py

# Ejecutar procesamiento completo post-streaming
./run_after_streaming.sh

Este script ejecuta:

Envío de datos por producer/api_to_kafka.py

Espera y transformación vía Spark

Conversión Parquet → CSV

Limpieza estática de CSV y PDF

Entrenamiento de modelos ML (Regresión Lineal y Random Forest)

Predicciones e inferencia

Copiado automático a Power BI

```
## 📊 Visualización final en Power BI

Dirígete a la carpeta output conecta Power BI a los archivos CSV necesarios para construir tu dashboard personalizado.

📷 Vista previa del Dashboard

![image](https://github.com/user-attachments/assets/1a1e4ade-ba48-49ef-80ea-af239573d592)


## 📌 Notas adicionales
Los archivos .pkl, .txt y .csv generados automáticamente se excluyen con .gitignore.

El sistema está optimizado para funcionar sin entorno gráfico (modo headless en WSL2).

El flujo completo es reproducible y automatizado desde run_after_streaming.sh.

## 👨‍🏫 Autor

**Güido Maidana**  
Apasionado por el análisis de datos, la automatización y la ingeniería de datos en tiempo real.

Este proyecto marca la transición hacia un entorno de trabajo profesional con **WSL2 + Ubuntu**, integrando tecnologías de **streaming**, **machine learning** y **visualización avanzada** para resolver desafíos del mundo financiero.

📬 ¿Comentarios o mejoras?  
¡Explora, clona y adapta este flujo completo a tus propios datos!
