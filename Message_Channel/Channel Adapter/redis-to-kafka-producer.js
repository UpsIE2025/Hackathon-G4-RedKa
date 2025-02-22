const { Kafka } = require("kafkajs");
const { createClient } = require("redis");

/**
 * Kafka instance configuration
 * @type {Kafka}
 */
const kafka = new Kafka({
    clientId: "redis-to-kafka-producer",
    brokers: ["localhost:9092"],
});

/**
 * Kafka producer instance
 * @type {import('kafkajs').Producer}
 */
const producer = kafka.producer();

/**
 * Redis client instance
 * @type {import('redis').RedisClientType}
 */
const redisClient = createClient();

(async () => {
    // Connect to Kafka and Redis
    await producer.connect();
    await redisClient.connect();
    console.log("Conectado a Kafka y Redis");

    // Subscribe to the Redis channel "message-channel"
    await redisClient.subscribe("message-channel", async (message) => {
        console.log("Mensaje recibido de Redis:", message);  // 🔹 Verifica si se recibe

        try {
            // Send the message to the Kafka topic "message-channel"
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