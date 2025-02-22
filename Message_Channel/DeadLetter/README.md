# Historia Técnica

## Título: Manejo de mensajes fallidos en campañas de marketing con Kafka y Redis

### Descripción:
Como ingeniero de software en el equipo de marketing, quiero que los mensajes fallidos sean enviados a Kafka y almacenados en Redis, para que puedan ser analizados en tiempo real y mejorar la efectividad de las campañas.

### Criterios de Aceptación:

- **DADO** que un correo o SMS no puede ser entregado,  
  **CUANDO** el servidor de mensajería detecta un error de entrega,  
  **ENTONCES** el mensaje debe publicarse en un topic de Kafka con información del fallo.

- **DADO** que un mensaje es publicado en Kafka,  
  **CUANDO** el Consumer lo procesa,  
  **ENTONCES** debe almacenarlo en Redis con detalles del usuario, canal de envío y motivo del fallo.

- **DADO** que el equipo de marketing necesita analizar los fallos en tiempo real,  
  **CUANDO** accede al dashboard de monitoreo,  
  **ENTONCES** debe visualizar estadísticas actualizadas desde Redis sobre las tasas de entrega y los errores más comunes.


