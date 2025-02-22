# Proyecto: Message Channel / Channel Adapter

Este proyecto implementa un **Message Channel** utilizando **Redis** y **Kafka** para el envío y recepción de mensajes entre aplicaciones. Utiliza **Docker Compose** para la infraestructura y **Node.js** con la librería `kafkajs` y `redis`.

---

## 📌 Caso de Uso Real: Sistema de Pedidos para un Restaurante 🍔

Supongamos que tenemos un sistema de pedidos en línea donde los clientes hacen pedidos a través de una aplicación web o móvil. Cada pedido debe ser procesado y enviado a la cocina para su preparación.

➡️ **¿Problema?**
Queremos desacoplar los diferentes módulos del sistema:
- **Frontend** (Cliente hace el pedido) 🛒
- **Backend** (Registra el pedido) 📦
- **Cocina** (Prepara el pedido) 👨‍🍳

➡️ **¿Solución?**
Utilizamos **Message Channel y Channel Adapter** con **Redis y Kafka** para garantizar una comunicación fluida entre estos módulos sin que dependan directamente unos de otros.

---

## 🚀 **Arquitectura**

1. **`docker-compose.yml`** → Define la infraestructura con Kafka, Redis y herramientas de monitoreo.
2. **`redis-publisher.js`** → Publica pedidos en un canal de Redis.
3. **`redis-to-kafka-producer.js`** → Suscribe a Redis y reenvía los pedidos a Kafka.
4. **`kafka-consumer.js`** → La cocina consume los pedidos desde Kafka y los procesa.

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

---

## 📝 **Archivos y su funcionalidad**

### 📌 `redis-publisher.js` → **Simulación de Pedidos**
Publica pedidos en el canal de Redis `order-channel`.

```js
const { createClient } = require("redis");
const generarPedido = () => ({
    idPedido: Math.floor(Math.random() * 1000),
    cliente: ["Juan Pérez", "María García", "Carlos Sánchez"][Math.floor(Math.random() * 3)],
    producto: ["Pizza", "Hamburguesa", "Papas Fritas"][Math.floor(Math.random() * 3)],
    cantidad: Math.floor(Math.random() * 5) + 1
});

const redisClient = createClient();
(async () => {
    await redisClient.connect();
    console.log("📦 Publicando pedidos en Redis...");
    for (let i = 0; i < 5; i++) {
        const pedido = generarPedido();
        await redisClient.publish("order-channel", JSON.stringify(pedido));
        console.log("✅ Pedido publicado:", pedido);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    await redisClient.disconnect();
})();
```

### 📌 `redis-to-kafka-producer.js` → **Redis → Kafka (Adaptador de Canal)**
Escucha pedidos en Redis y los reenvía a Kafka.

```js
const { Kafka } = require("kafkajs");
const { createClient } = require("redis");
const kafka = new Kafka({ clientId: "redis-to-kafka-producer", brokers: ["localhost:9092"] });
const producer = kafka.producer();
const redisClient = createClient();
(async () => {
    await producer.connect();
    await redisClient.connect();
    console.log("🔄 Conectado a Redis y Kafka");
    await redisClient.subscribe("order-channel", async (pedido) => {
        console.log("📦 Pedido recibido de Redis:", pedido);
        try {
            await producer.send({ topic: "order-channel", messages: [{ value: pedido }] });
            console.log("✅ Pedido enviado a Kafka:", pedido);
        } catch (error) {
            console.error("❌ Error enviando pedido a Kafka:", error);
        }
    });
})();
```

### 📌 `kafka-consumer.js` → **Consumidor de Kafka (Cocina)**
Recibe pedidos y los procesa.

```js
const { Kafka } = require("kafkajs");
const kafka = new Kafka({ clientId: "kafka-consumer", brokers: ["localhost:9092"] });
const consumer = kafka.consumer({ groupId: "cocina-orders" });
(async () => {
    await consumer.connect();
    await consumer.subscribe({ topic: "order-channel", fromBeginning: true });
    console.log("👨‍🍳 Cocina lista para recibir pedidos...");
    await consumer.run({
        eachMessage: async ({ message }) => {
            const pedido = JSON.parse(message.value.toString());
            console.log(`🍔 Preparando pedido #${pedido.idPedido} (${pedido.cantidad}x ${pedido.producto} para ${pedido.cliente})...`);
            await new Promise(resolve => setTimeout(resolve, Math.random() * 5000 + 2000));
            console.log(`✅ Pedido #${pedido.idPedido} de ${pedido.cliente} listo para entrega.`);
        },
    });
})();
```

---

📌 **Este sistema desacopla los módulos del restaurante y permite que los pedidos se procesen en tiempo real sin bloquear otras operaciones. 🚀**


---
📌 **¿Qué es un Message Channel y un Channel Adapter?**

**Message Channel**  
Es un medio a través del cual las aplicaciones pueden enviar y recibir mensajes de forma desacoplada. En este caso, usamos Redis y Kafka como canales de mensajería.

**Channel Adapter**  
Es un adaptador que permite que una aplicación se conecte a un Message Channel sin que esta tenga que saber nada sobre el canal en sí. Actúa como un "puente" entre la aplicación y el sistema de mensajería.  

