# Historia de Usuario

**Como** arquitecto de software,  
**Quiero** garantizar la entrega de mensajes en Kafka mediante un canal de mensajes con persistencia,  
**Para** asegurar que los mensajes no se pierdan incluso en caso de falla del sistema de mensajería.

# Criterios de Aceptación

### Persistencia de Mensajes
- **DADO** que un productor envía un mensaje a un tópico en Kafka,  
  **CUANDO** el mensaje es recibido por un broker,  
  **ENTONCES** este debe ser almacenado de forma persistente en el log de mensajes antes de confirmar la recepción al productor.  

### Confirmación de Procesamiento
- **DADO** que un mensaje ha sido almacenado en un broker,  
  **CUANDO** un consumidor intenta procesarlo,  
  **ENTONCES** el mensaje no se elimina del log hasta que el consumidor confirme su procesamiento exitoso.  

### Tolerancia a Fallos
- **DADO** que un broker de Kafka falla,  
  **CUANDO** hay réplicas del log en otros brokers,  
  **ENTONCES** los mensajes deben poder recuperarse desde las réplicas sin pérdida de datos.  