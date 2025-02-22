# Proyecto: Message Channel / Channel Adapter

Este proyecto implementa un **Message Channel** utilizando **Redis** y **Kafka** para el envío y recepción de mensajes entre aplicaciones. Utiliza **Docker Compose** para la infraestructura y **Node.js** con la librería `kafkajs` y `redis`.

---

## 🚀 **Arquitectura**

1. **`docker-compose.yml`** → Define la infraestructura con Kafka, Redis y herramientas de monitoreo.
2. **`redis-publisher.js`** → Publica mensajes en un canal de Redis.
3. **`redis-to-kafka-producer.js`** → Suscribe a Redis y reenvía los mensajes a Kafka.
4. **`kafka-consumer.js`** → Consume los mensajes desde Kafka.

---

## 📦 **Infraestructura con Docker Compose**

El archivo `docker-compose.yml` define los siguientes servicios:

```yaml
services:
  kafka:
    image: apache/kafka:latest
    container_name: broker
    hostname: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://localhost:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_NUM_PARTITIONS: 3
    networks:
      - default

  redis:
    image: redis:latest
    container_name: redis-broker
    ports:
      - "6379:6379"
    networks:
      - default

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: redis-commander
    ports:
      - "8081:8081"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
    networks:
      - default

networks:
  default:
    driver: bridge
```

### 🔹 **Explicación de los servicios:**
- **Kafka (`broker`)**: Maneja la comunicación asincrónica basada en eventos.
- **Redis (`redis-broker`)**: Almacena y publica mensajes en un canal de Redis.
- **Redis Commander (`redis-commander`)**: Provee una interfaz web para monitorear Redis en `http://localhost:8081`.

---

## 📝 **Archivos y su funcionalidad**

### 📌 `redis-publisher.js` → **Publicador en Redis**
Publica mensajes en el canal de Redis `message-channel`.

```js
const { createClient } = require("redis");
const axios = require("axios");

const redisClient = createClient();
(async () => {
    await redisClient.connect();
    console.log("📡 Conectado a Redis");

    const response = await axios.get("https://jsonplaceholder.typicode.com/posts/1");
    const message = JSON.stringify(response.data);

    await redisClient.publish("message-channel", message);
    console.log("📨 Mensaje publicado en Redis:", message);

    await redisClient.disconnect();
})();
```

---

### 📌 `redis-to-kafka-producer.js` → **Redis → Kafka**
Escucha mensajes en Redis y los reenvía a Kafka.

```js
const { Kafka } = require("kafkajs");
const { createClient } = require("redis");

const kafka = new Kafka({
    clientId: "redis-to-kafka-producer",
    brokers: ["localhost:9092"],
});

const producer = kafka.producer();
const redisClient = createClient();

(async () => {
    await producer.connect();
    await redisClient.connect();
    console.log("🔄 Conectado a Kafka y Redis");

    await redisClient.subscribe("message-channel", async (message) => {
        console.log("📥 Mensaje recibido de Redis:", message);
        try {
            await producer.send({
                topic: "message-channel",
                messages: [{ value: message }],
            });
            console.log("✅ Mensaje enviado a Kafka:", message);
        } catch (error) {
            console.error("❌ Error enviando mensaje a Kafka:", error);
        }
    });
})();
```

---

### 📌 `kafka-consumer.js` → **Consumidor de Kafka**
Escucha mensajes en Kafka y los procesa.

```js
const { Kafka } = require("kafkajs");

const kafka = new Kafka({
    clientId: "kafka-consumer",
    brokers: ["localhost:9092"],
});

const consumer = kafka.consumer({ groupId: "message-consumers" });

const run = async () => {
    await consumer.connect();
    console.log("📥 Conectado a Kafka como consumer");

    await consumer.subscribe({ topic: "message-channel", fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            console.log(`📩 Mensaje recibido desde Kafka: ${message.value.toString()}`);
        },
    });
};

run().catch(async (error) => {
    console.error("❌ Error en el consumidor:", error);
    console.log("🔄 Reintentando en 5 segundos...");
    setTimeout(run, 5000);
});
```

---

## 🔧 **Cómo ejecutar**

### 1️⃣ **Levantar los contenedores**
```bash
docker-compose up -d
```

### 2️⃣ **Verificar que Redis y Kafka están corriendo**
```bash
redis-cli ping
```
Debe responder `PONG`.
```bash
nc -zv localhost 9092
```
Debe decir `Connection succeeded!`.

### 3️⃣ **Publicar un mensaje en Redis**
```bash
node redis-publisher.js
```

### 4️⃣ **Escuchar mensajes de Redis y reenviarlos a Kafka**
```bash
node redis-to-kafka-producer.js
```

### 5️⃣ **Consumir los mensajes de Kafka**
```bash
node kafka-consumer.js
```

---

## 🎯 **Resumen del flujo de datos**
1. `redis-publisher.js` **publica** un mensaje en **Redis**.
2. `redis-to-kafka-producer.js` **escucha** ese mensaje y lo reenvía a **Kafka**.
3. `kafka-consumer.js` **consume** el mensaje desde **Kafka**.

---

## 🎉 **Conclusión**
Este proyecto demuestra cómo Redis y Kafka pueden integrarse para permitir un **Message Channel**, facilitando la comunicación entre servicios de manera escalable y desacoplada.

🚀 ¡Ahora puedes modificarlo para adaptarlo a tus necesidades! 🔥

