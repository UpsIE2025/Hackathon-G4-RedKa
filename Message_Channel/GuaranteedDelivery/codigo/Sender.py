from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092', 'acks': 'all'}
producer = Producer(conf)

def delivery_report(err, msg):
    if err:
        print(f'Error al enviar mensaje: {err}')
    else:
        print(f'Mensaje enviado a {msg.topic()} [{msg.partition()}]')

for i in range(5):
    producer.produce('mensaje-seguro', key=str(i), value=f'Mensaje {i}', callback=delivery_report)

producer.flush()
