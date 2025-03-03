# Document Message

Este proyecto implementa el patrón **Document Message** utilizando **Node.js** y **RabbitMQ** para enviar y recibir estructuras de datos en colas de mensajería.

## 📌 Instalación y Uso

1. Clonar el repositorio
2. Instalar dependencias con npm install

---

## Uso
El consumidor estará esperando mensajes en la cola `document_messages`. Si se recibe un mensaje, se mostrará en la consola.

---

## Configuración con Docker
Si no tienes RabbitMQ instalado localmente, puedes ejecutarlo con Docker:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Esto ejecutará RabbitMQ con la interfaz web disponible en **http://localhost:15672** (Usuario: `guest`, Contraseña: `guest`).

---

## Prueba con cURL

Para enviar mensajes JSON a la cola `document_messages`, usa **cURL**:
```bash
curl --location 'http://localhost:15672/api/exchanges/%2F/amq.default/publish' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46YWRtaW4=' \
--data '{"properties":{},"routing_key":"document_messages","payload":"{\"id\":\"DOC123\",\"type\":\"Purchase Order\",\"content\":{\"customer\":\"John Doe\",\"items\":[{\"product\":\"Laptop\",\"quantity\":1,\"price\":1200},{\"product\":\"Mouse\",\"quantity\":2,\"price\":25}],\"total\":1250}}","payload_encoding":"string"}'
```

## Ejecutar el Proyecto

Local:
1. Correr el docker de RabbitMQ
2. Después de instalar las dependencias, inicia el proyecto con:
```bash
npm start
```

Dockerizado:
1. Ejecutar 
```bash
docker-compose up --build
```
2. Consumir el CURL