require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const { sendDocumentMessage, receiveDocumentMessage } = require('./services/documentMessage');

const app = express();
const PORT = process.env.PORT;

app.use(bodyParser.json());

// Ruta para recibir documentos vía HTTP y enviarlos a RabbitMQ
app.post('/send-document', async (req, res) => {
    try {
        const document = req.body;
        if (!document || Object.keys(document).length === 0) {
            return res.status(400).json({ error: 'Documento invalido' });
        }
        
        await sendDocumentMessage(document);
        res.status(200).json({ message: 'Documento enviado correctamente', document });
    } catch (error) {
        res.status(500).json({ error: 'Error sending document', details: error.message });
    }
});

// Iniciar el consumidor de mensajes (recibe documentos)
receiveDocumentMessage();

app.listen(PORT, () => {
    console.log(`Document Message API corriendo en http://localhost:${PORT}`);
});
