const { createClient } = require("redis");
const axios = require("axios");

const client = createClient({
    url: "redis://localhost:6379"
});

client.on("error", (err) => console.error("Redis Client Error", err));

const publishToRedis = async () => {
    await client.connect();  // Conectar a Redis antes de usarlo

    try {
        const response = await axios.get("https://jsonplaceholder.typicode.com/posts/1");
        const message = JSON.stringify(response.data);

        await client.publish("message-channel", message);
        console.log("Mensaje publicado en Redis:", message);

    } catch (error) {
        console.error("Error publicando en Redis:", error);
    } finally {
        await client.quit();  // Cerrar la conexión después de enviar el mensaje
    }
};

publishToRedis();
