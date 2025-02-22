import time
import json
import os
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from fastapi import FastAPI
from pydantic import BaseModel

# Configuración de Kafka
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = "address-changes"

# Inicializar FastAPI
app = FastAPI()

# Modelo de datos para la API
class Event(BaseModel):
    event: str
    timestamp: str

# Esperar hasta que Kafka esté listo
attempts = 0
while attempts < 10:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print(f"✅ Conectado a Kafka en {KAFKA_BROKER}")
        break
    except NoBrokersAvailable:
        attempts += 1
        print(f"⚠️ Esperando a Kafka... Intento {attempts}/10")
        time.sleep(5)

if attempts == 10:
    print("❌ No se pudo conectar a Kafka después de 10 intentos. Saliendo.")
    exit(1)

@app.post("/publish")
def publish_event(event: Event):
    try:
        message = {"event": event.event, "timestamp": event.timestamp}
        producer.send(TOPIC, value=message)
        print(f"📤 Evento enviado: {message}")
        return {"message": "Evento enviado correctamente", "data": message}
    except Exception as e:
        print(f"❌ Error al enviar evento: {e}")
        return {"error": "No se pudo enviar el evento"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
