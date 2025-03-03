const connectRabbitMQ = require('../config/rabbitmq');

const SOURCE_QUEUE = process.env.SOURCE_QUEUE;
const DESTINATION_QUEUE = process.env.DESTINATION_QUEUE;

async function messagingBridge() {
    try {
        const channel = await connectRabbitMQ();
        await channel.assertQueue(SOURCE_QUEUE, { durable: true });
        await channel.assertQueue(DESTINATION_QUEUE, { durable: true });

        console.log(`Escuchando mensajes en ${SOURCE_QUEUE}...`);

        channel.consume(SOURCE_QUEUE, async (message) => {
            if (message) {
                console.log(`Recibido: ${message.content.toString()}`);
                const transformedMessage = message.content.toString().toUpperCase();
                channel.sendToQueue(DESTINATION_QUEUE, Buffer.from(transformedMessage), { persistent: true });
                console.log(`Reenviado a ${DESTINATION_QUEUE}: ${transformedMessage}`);
                channel.ack(message);
            }
        });
    } catch (error) {
        console.error('Error in messaging bridge:', error);
    }
}

module.exports = messagingBridge;