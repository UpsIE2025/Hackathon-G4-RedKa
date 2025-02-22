from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Configurar el producer Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = 'valid-messages'  # Tema para mensajes válidos

@app.route('/produce', methods=['POST'])
def produce_message():
    data = request.json

    # Validación: asegurarse de que el mensaje tiene el formato correcto
    #Nota comentar este segmento de código si se ejecuta el script consumerdir.py
    if 'id' not in data or 'content' not in data:
        # Si el mensaje es inválido, enviarlo al canal de mensajes no válidos
        producer.send('invalid-messages', {'error': 'Formato incorrecto', 'message': data})
        return jsonify({'status': 'error', 'message': 'Mensaje inválido enviado a invalid-messages'}), 400

    # Si el mensaje es válido, enviarlo al topic correcto
    producer.send(TOPIC, data)
    return jsonify({'status': 'success', 'message': 'Mensaje enviado correctamente'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
