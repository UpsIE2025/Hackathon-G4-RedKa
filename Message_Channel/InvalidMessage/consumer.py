from kafka import KafkaConsumer, KafkaProducer
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Consumer para mensajes válidos
consumer = KafkaConsumer(
    'valid-messages',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consumer para mensajes inválidos
invalid_consumer = KafkaConsumer(
    'invalid-messages',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Producer para reenviar mensajes corregidos
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Procesar mensajes válidos
def process_valid_messages():
    for message in consumer:
        logging.info(f"Procesando mensaje válido: {message.value}")

# Procesar mensajes inválidos y reenviarlos si se corrigen
def process_invalid_messages():
    for message in invalid_consumer:
        logging.warning(f"Mensaje inválido recibido: {message.value}")
        
        # Lógica para reprocesar un mensaje (simulación)
        corrected_message = message.value.get('message')
        if corrected_message:
            logging.info("Corrigiendo mensaje y reenviándolo...")
            producer.send('valid-messages', corrected_message)

# Iniciar consumers
if __name__ == '__main__':
    import threading

    threading.Thread(target=process_valid_messages, daemon=True).start()
    threading.Thread(target=process_invalid_messages, daemon=True).start()

    input("Presiona Enter para salir...\n")
