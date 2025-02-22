const { Kafka } = require("kafkajs");
const { createClient } = require("redis");

// Configurar Kafka
const kafka = new Kafka({
    clientId: "redis-to-kafka-producer",
    brokers: ["localhost:9092"],
});

const producer = kafka.producer();
const redisClient = createClient();

(async () => {
    await producer.connect();
    await redisClient.connect();
    console.log("🔄 Conectado a Redis y Kafka");

    await redisClient.subscribe("order-channel", async (pedido) => {
        console.log("📦 Pedido recibido de Redis:", pedido);

        try {
            await producer.send({
                topic: "order-channel",
                messages: [{ value: pedido }],
            });

            console.log("✅ Pedido enviado a Kafka:", pedido);
        } catch (error) {
            console.error("❌ Error enviando pedido a Kafka:", error);
        }
    });
})();
