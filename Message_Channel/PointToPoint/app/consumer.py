from kafka import KafkaConsumer


def main():
    try:
        consumer = KafkaConsumer(
            'point_to_point',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',  # Lee desde el inicio si es un consumidor nuevo
            enable_auto_commit=True,  # Confirma automáticamente la lectura de los mensajes
            group_id='grupo_consumidores_p2p'  # Grupo de consumidores
        )

        print("Esperando mensajes en el tópico 'telegrafo'...")

        for msg in consumer:
            print(f"Mensaje recibido: {msg.value.decode('utf-8')}")

    except Exception as e:
        print(f"Error en el consumidor: {e}")


if __name__ == '__main__':
    main()
