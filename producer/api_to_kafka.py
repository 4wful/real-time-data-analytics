import json
import time
import requests
import os
import sys
from kafka import KafkaProducer

# === Agregar la raíz del proyecto al sys.path ===
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# === Cargar variables del .env manualmente desde la raíz ===
env_path = os.path.join(ROOT_DIR, '.env')

if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
else:
    raise FileNotFoundError(f"No se encontró el archivo .env en: {env_path}")

API_KEY = os.environ.get("API_KEY")
TOPIC = os.environ.get("KAFKA_TOPIC")
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS").split(",")

BASE_URL = "https://www.alphavantage.co/query"

def get_intraday(symbol, interval="5min", outputsize="compact"):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY,
        "outputsize": outputsize,
        "datatype": "json"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if "Error Message" in data:
        print(f"Error: {data['Error Message']}")
        return None
    if "Note" in data:
        print(f"API call limit reached: {data['Note']}")
        return None
    return data

def main():
    symbol = "NVDA"
    data = get_intraday(symbol)
    if not data:
        print("No data fetched from API.")
        return

    time_series_key = next((key for key in data if "Time Series" in key), None)
    if not time_series_key:
        print("No time series data found.")
        return

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for timestamp, values in data[time_series_key].items():
        message = {
            "symbol": symbol,
            "timestamp": timestamp,
            "open": values['1. open'],
            "high": values['2. high'],
            "low": values['3. low'],
            "close": values['4. close'],
            "volume": values['5. volume']
        }
        producer.send(TOPIC, value=message)
        print(f"📤 Enviado mensaje para {timestamp}")

    producer.flush()
    producer.close()
    print("✅ Todos los mensajes enviados.")

if __name__ == "__main__":
    main()
