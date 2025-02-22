const { createClient } = require("redis");

// Generador de pedidos aleatorios
const generarPedido = () => ({
    idPedido: Math.floor(Math.random() * 1000),
    cliente: ["Juan Pérez", "María García", "Carlos Sánchez", "Ana Fernández"][Math.floor(Math.random() * 4)],
    producto: ["Hamburguesa Doble", "Pizza", "Papas Fritas", "Hot Dog"][Math.floor(Math.random() * 4)],
    cantidad: Math.floor(Math.random() * 5) + 1,
    estado: "Pendiente"
});

// Conectar a Redis
const redisClient = createClient();

(async () => {
    await redisClient.connect();
    console.log("📦 Publicando pedidos en Redis...");

    for (let i = 0; i < 5; i++) {
        const pedido = generarPedido();
        await redisClient.publish("order-channel", JSON.stringify(pedido));
        console.log("✅ Pedido publicado:", pedido);

        // Simulación de envío escalonado
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    await redisClient.disconnect();
})();
