const { Kafka } = require("kafkajs");

// Configuración de Kafka
const kafka = new Kafka({
    clientId: "kafka-consumer",
    brokers: ["localhost:9092"]
});

const consumer = kafka.consumer({ groupId: "message-consumers" });

const startConsumer = async () => {
    await consumer.connect();
    await consumer.subscribe({ topic: "message-channel", fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            console.log(`Mensaje recibido desde Kafka: ${message.value.toString()}`);
        }
    });
};

startConsumer();
