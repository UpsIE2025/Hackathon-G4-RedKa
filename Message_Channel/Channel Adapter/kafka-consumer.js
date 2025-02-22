const { Kafka } = require("kafkajs");

/**
 * Kafka configuration
 * @type {Kafka}
 */
const kafka = new Kafka({
    clientId: "kafka-consumer",
    brokers: ["localhost:9092"]
});

/**
 * Kafka consumer instance
 * @type {import('kafkajs').Consumer}
 */
const consumer = kafka.consumer({ groupId: "message-consumers" });

/**
 * Starts the Kafka consumer, subscribes to the topic, and processes incoming messages.
 * @async
 * @function startConsumer
 * @returns {Promise<void>}
 */
const startConsumer = async () => {
    // Connect to the Kafka broker
    await consumer.connect();

    // Subscribe to the topic "message-channel" from the beginning
    await consumer.subscribe({ topic: "message-channel", fromBeginning: true });

    // Run the consumer to process each message
    await consumer.run({
        /**
         * Processes each message received from Kafka.
         * @async
         * @function eachMessage
         * @param {Object} param0 - The message object
         * @param {string} param0.topic - The topic name
         * @param {number} param0.partition - The partition number
         * @param {import('kafkajs').Message} param0.message - The Kafka message
         */
        eachMessage: async ({ topic, partition, message }) => {
            console.log(`Mensaje recibido desde Kafka: ${message.value.toString()}`);
        }
    });
};

// Start the Kafka consumer
startConsumer();