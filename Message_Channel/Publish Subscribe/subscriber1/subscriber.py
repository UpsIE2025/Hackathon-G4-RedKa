from kafka import KafkaConsumer
import redis
import json
import os

# Configuración de Kafka y Redis
KAFKA_BROKER = 'kafka:9092'
TOPIC = "address-changes"
REDIS_HOST = 'redis'
REDIS_PORT = 6379
SUBSCRIBER_ID = os.getenv("SUBSCRIBER_ID", "subscriber1")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

for message in consumer:
    event = message.value
    event_id = event["timestamp"]

    # Verificar si el evento ya fue consumido por este suscriptor
    if redis_client.sismember(SUBSCRIBER_ID, event_id):
        continue  # Saltar eventos ya procesados

    # Procesar el evento
    print(f"[{SUBSCRIBER_ID}] 🔔 Evento recibido: {event}")

    # Marcar el evento como procesado en Redis
    redis_client.sadd(SUBSCRIBER_ID, event_id)
