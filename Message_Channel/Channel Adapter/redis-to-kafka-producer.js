const { Kafka } = require("kafkajs");
const { createClient } = require("redis");

const kafka = new Kafka({
    clientId: "redis-to-kafka-producer",
    brokers: ["localhost:9092"],
});


const producer = kafka.producer();
const redisClient = createClient();

(async () => {
    await producer.connect();
    await redisClient.connect();
    console.log("Conectado a Kafka y Redis");

    await redisClient.subscribe("message-channel", async (message) => {
        console.log("Mensaje recibido de Redis:", message);  // 🔹 Verifica si se recibe

        try {
            await producer.send({
                topic: "message-channel",
                messages: [{ value: message }],
            });

            console.log("✅ Mensaje enviado a Kafka:", message);  // 🔹 Verifica si se envió correctamente
        } catch (error) {
            console.error("❌ Error enviando mensaje a Kafka:", error);
        }
    });
})();
