from confluent_kafka import Consumer, KafkaException

conf = {
    'bootstrap.servers': 'kafka-1:9092',
    'group.id': 'grupo-consumidor',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

consumer = Consumer(conf)
consumer.subscribe(['mensaje-seguro'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        print(f'Recibido: {msg.value().decode("utf-8")}')

        consumer.commit()
except KeyboardInterrupt:
    print("\nCerrando consumidor...")
finally:
    consumer.close()