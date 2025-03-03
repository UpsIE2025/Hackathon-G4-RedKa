# Messaging Bridge

Este proyecto implementa un puente de mensajería entre dos sistemas de mensajería utilizando RabbitMQ en Node.js.

## Instalación
1. Clonar el repositorio
2. Instalar dependencias con `npm install`


## Uso
Este servicio escucha en la cola `source_queue`, transforma los mensajes y los reenvía a `destination_queue`. 

## Configuración con Docker
Si no tienes RabbitMQ instalado localmente, puedes ejecutarlo con Docker:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

Esto ejecutará RabbitMQ con la interfaz web disponible en **http://localhost:15672** (Usuario: `guest`, Contraseña: `guest`).

## Prueba con cURL
Puedes enviar un mensaje de prueba a `emisor_user` usando la API de RabbitMQ con el siguiente comando:

```bash
curl --location 'http://localhost:15672/api/exchanges/%2F/amq.default/publish' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic Z3Vlc3Q6Z3Vlc3Q=' \
--data '{"properties":{},"routing_key":"emisor_user","payload":"Hola receptor","payload_encoding":"string"}'
```

## Ejecutar el Proyecto

Local:
Correr el docker de RabbitMQ
Después de instalar las dependencias, inicia el proyecto con:
```bash
npm start
```

Dockerizado
Ejecutar docker-compose up --build
Consumir el CURL