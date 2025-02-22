import time
import json
import os
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import redis
from fastapi import FastAPI

# Configuración de Kafka y Redis
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = "address-changes"
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
SUBSCRIBER_ID = os.getenv("SUBSCRIBER_ID", "subscriber1")

# Inicializar FastAPI
app = FastAPI()

# Conectar a Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, decode_responses=True)

# Esperar hasta que Kafka esté listo
attempts = 0
while attempts < 10:
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=SUBSCRIBER_ID
        )
        print(f"✅ [{SUBSCRIBER_ID}] Conectado a Kafka en {KAFKA_BROKER}")
        break
    except NoBrokersAvailable:
        attempts += 1
        print(f"⚠️ [{SUBSCRIBER_ID}] Esperando a Kafka... Intento {attempts}/10")
        time.sleep(5)

if attempts == 10:
    print(f"❌ [{SUBSCRIBER_ID}] No se pudo conectar a Kafka. Saliendo.")
    exit(1)

# Consumir mensajes en segundo plano
def consume_messages():
    for message in consumer:
        event = message.value
        event_id = event.get("timestamp", message.offset)

        # Evitar procesar el mismo evento dos veces
        if redis_client.sismember(SUBSCRIBER_ID, event_id):
            continue

        print(f"🔔 [{SUBSCRIBER_ID}] Evento recibido: {event}")
        redis_client.sadd(SUBSCRIBER_ID, event_id)
        print(f"✅ [{SUBSCRIBER_ID}] Evento guardado en Redis con ID: {event_id}")

# Endpoint para obtener eventos almacenados
@app.get("/events")
def get_events():
    events = redis_client.smembers(SUBSCRIBER_ID)
    return {"subscriber": SUBSCRIBER_ID, "events": list(events)}

# Iniciar consumidor en segundo plano
import threading
threading.Thread(target=consume_messages, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
