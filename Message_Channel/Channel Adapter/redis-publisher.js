const { createClient } = require("redis");
const axios = require("axios");

/**
 * Redis client instance
 * @type {import('redis').RedisClientType}
 */
const client = createClient({
    url: "redis://localhost:6379"
});

client.on("error", (err) => console.error("Redis Client Error", err));

/**
 * Publishes a message to a Redis channel after fetching data from an external API.
 * @async
 * @function publishToRedis
 * @returns {Promise<void>}
 */
const publishToRedis = async () => {
    await client.connect();  // Connect to Redis before using it

    try {
        const response = await axios.get("https://jsonplaceholder.typicode.com/posts/1");
        const message = JSON.stringify(response.data);

        await client.publish("message-channel", message);
        console.log("Message published to Redis:", message);

    } catch (error) {
        console.error("Error publishing to Redis:", error);
    } finally {
        await client.quit();  // Close the connection after sending the message
    }
};

// Start the process of publishing to Redis
publishToRedis();