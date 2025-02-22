from kafka import KafkaConsumer
import json
import time
import logging

logging.basicConfig(level=logging.INFO)

INVALID_MESSAGES_THRESHOLD = 5  # Número de mensajes inválidos antes de generar alerta

def monitor_invalid_messages():
    consumer = KafkaConsumer(
        'invalid-messages',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    invalid_count = 0

    for message in consumer:
        invalid_count += 1
        logging.warning(f"Mensaje inválido detectado: {message.value}")

        if invalid_count >= INVALID_MESSAGES_THRESHOLD:
            logging.error("⚠️ ALERTA: Se han recibido demasiados mensajes inválidos en Kafka!")
            invalid_count = 0  # Reiniciar contador después de la alerta

if __name__ == '__main__':
    monitor_invalid_messages()
