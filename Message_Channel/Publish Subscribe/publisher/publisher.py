from kafka import KafkaProducer
import json
import time

# Configuración del productor Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "address-changes"

def publish_event():
    event = {
        "event": "Address Changed",
        "timestamp": time.time()
    }
    producer.send(TOPIC, event)
    print(f"[✔] Evento publicado: {event}")

if __name__ == "__main__":
    while True:
        publish_event()
        time.sleep(5)  # Publicar cada 5 segundos
