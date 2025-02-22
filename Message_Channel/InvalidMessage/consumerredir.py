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
        logging.info(f"Procesando mensaje: {message.value}")
        # Validación: verifica si el mensaje tiene formato correcto
        if 'id' not in message.value or 'content' not in message.value:
            # Si el mensaje es inválido, enviarlo al canal de mensajes no válidos
            producer.send('invalid-messages', {'error': 'Formato incorrecto', 'message': message.value})
            logging.warning(f"Mensaje inválido enviado a invalid-messages: {message.value}")

        else:
            logging.info(f"Mensaje válido: {message.value}")

if __name__ == '__main__':
    process_valid_messages()
