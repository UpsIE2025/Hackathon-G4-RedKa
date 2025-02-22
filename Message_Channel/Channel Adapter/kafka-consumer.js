const { Kafka } = require("kafkajs");

// Configurar Kafka
const kafka = new Kafka({
    clientId: "kafka-consumer",
    brokers: ["localhost:9092"],
});

const consumer = kafka.consumer({ groupId: "cocina-orders" });

(async () => {
    await consumer.connect();
    await consumer.subscribe({ topic: "order-channel", fromBeginning: true });

    console.log("👨‍🍳 Cocina lista para recibir pedidos...");

    await consumer.run({
        eachMessage: async ({ message }) => {
            const pedido = JSON.parse(message.value.toString());
            console.log(`🍔 Preparando pedido #${pedido.idPedido} (${pedido.cantidad}x ${pedido.producto} para ${pedido.cliente})...`);

            // Simulación de tiempo de preparación
            await new Promise(resolve => setTimeout(resolve, Math.random() * 5000 + 2000));

            console.log(`✅ Pedido #${pedido.idPedido} de ${pedido.cliente} listo para entrega.`);
        },
    });
})();
