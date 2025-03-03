const amqp = require('amqplib');
const BROKER_URL = process.env.BROKER_URL;

async function connectRabbitMQ() {
    const connection = await amqp.connect(BROKER_URL);
    return await connection.createChannel();
}

module.exports = connectRabbitMQ;