# 📈 Proyecto: Análisis Financiero con Streaming y Power BI (Business Analytics)

Este repositorio contiene un sistema de análisis de datos bursátiles con procesamiento de datos en tiempo real y visualización avanzada en **Power BI**. Está orientado al curso de Business Analytics, con foco en generar insights útiles para la toma de decisiones empresariales.

---

## 🛠️ Tecnologías utilizadas

- **Apache Kafka**: streaming de datos financieros  
- **Apache Spark**: procesamiento ETL en tiempo real  
- **Python**: transformación, modelado y predicción  
- **Power BI**: visualización de KPIs, métricas e insights  
- **Docker**: orquestación de contenedores (Kafka)

## 📁 Estructura general del proyecto

```
├── config/ # Rutas y configuración
├── kafka_services/ # Docker Compose 
├── machine_learning/ # Entrenamiento y predicción de modelos ML
├── output/ # Datos procesados (Parquet/CSV/ZIP)                
├── power_bi/ # Reporte Power BI (.pbix)             
├── producer/ # Scripts para enviar datos a Kafka
├── raw_data/  # Datos crudos (CSV y PDF)             
├── spark/ # Procesamiento en streaming con Spark
├── static_etl/ # Procesamiento para datos estáticos
├── utils/ # Utilidades (conversión, helpers)
├── venv/ ⚠️ No incluido: entorno virtual local 
├── .env ⚠️ No incluido: debes crearlo localmente con tus variables sensibles
├── .gitignore # Archivos/carpetas ignorados por Git 
├── check_env.py # Verificador de variables de entorno
├── Readme.markdown # Documentación general                
└── requirements.txt # Dependencias del proyecto
```

## 🧰 Requisitos del sistema

Instala los siguientes componentes antes de ejecutar el proyecto:

- Python 3.8+  
- Java JDK 8 ✅ obligatorio para Spark  
- Apache Hadoop (cliente local)  
- Apache Spark (local)  
- Docker Desktop (para correr Kafka/Zookeeper)  
- Power BI Desktop (para abrir los reportes)

## 🚀 Pasos para ejecutar el proyecto

### 1. Clonar y preparar entorno

```bash
git clone https://github.com/4wful/real-time-data-analytics.git
cd real-time-data-analytics
python -m venv venv
source .\venv\Scripts\Activate.ps1 
pip install -r requirements.txt
```

### 2. Configurar variables sensibles

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
API_KEY=tu_api_key_aqui  # (ALPHA VANTAGE API)
KAFKA_TOPIC=nombre_de_tu_topic
KAFKA_BOOTSTRAP_SERVERS=tus_local_host
```

### 3. Levantar servicios Kafka

```bash
cd kafka_services
docker-compose up --build
```

Crear y verificar el tópico:

```bash
# Crear tópico
docker exec -it kafka-broker-1 kafka-topics --create \
  --bootstrap-server kafka-broker-1:29092 \
  --replication-factor 3 --partitions 3 \
  --topic mercados-bursatiles --if-not-exists

# Verificar tópicos
docker exec -it kafka-broker-1 kafka-topics --list \
  --bootstrap-server kafka-broker-1:29092
```

### 4. Ejecutar el flujo de datos

```bash
# a. Enviar datos a Kafka
python producer/api_to_kafka.py

# b. Procesar datos en Spark Streaming
.\run_spark_api.ps1

# c. Conversión Parquet a CSV
.\run_parquet_csv.ps1

# d. ETL estático desde PDF
.\run_static_etl.ps1
```

### 5. Modelo de predicción (opcional)

```bash
python machine_learning/model_train.py
python machine_learning/inference.py
```

## 📊 Visualización final en Power BI

Dirígete a la carpeta `output/dashboard_data/` y conecta Power BI al archivo CSV para construir tu dashboard personalizado.

📌 *Próximamente se añadirá una imagen de referencia del dashboard final.*

**Ejemplo de KPIs sugeridos:**

- Predicción de precios de acciones  
- Volumen negociado  
- Comparativas por trimestre o región

---

## 👨‍🏫 Autor

**Grupo 4** – Trabajo final para el curso **Business Analytics** (Año 2025), dictado por el docente **Lira Camacho**.

¡Explora, ejecuta y aprende del flujo completo de datos en tiempo real! 📈

> **Todos los derechos reservados al Grupo 4.**
