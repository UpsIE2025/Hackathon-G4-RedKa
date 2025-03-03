const amqp = require('amqplib');

const BROKER_URL = process.env.BROKER_URL;
const DOCUMENT_QUEUE = process.env.DOCUMENT_QUEUE;

async function sendDocumentMessage(document) {
    try {
        const connection = await amqp.connect(BROKER_URL);
        const channel = await connection.createChannel();

        await channel.assertQueue(DOCUMENT_QUEUE, { durable: true });
        channel.sendToQueue(DOCUMENT_QUEUE, Buffer.from(JSON.stringify(document)), { persistent: true });
        
        console.log(`Documento enviado: ${JSON.stringify(document)}`);
        await channel.close();
        await connection.close();
    } catch (error) {
        console.error('Error sending document message:', error);
    }
}

async function receiveDocumentMessage() {
    try {
        const connection = await amqp.connect(BROKER_URL);
        const channel = await connection.createChannel();

        await channel.assertQueue(DOCUMENT_QUEUE, { durable: true });
        console.log(`Esperando mensajes de documentos en ${DOCUMENT_QUEUE}...`);

        channel.consume(DOCUMENT_QUEUE, (message) => {
            if (message) {
                const document = JSON.parse(message.content.toString());
                console.log(`Documento recibido:`, document);
                channel.ack(message);
            }
        });
    } catch (error) {
        console.error('Error receiving document message:', error);
    }
}

module.exports = { sendDocumentMessage, receiveDocumentMessage };
