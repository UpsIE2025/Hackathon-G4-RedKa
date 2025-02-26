# 🎯 Historia de Usuario

**COMO** desarrollador de sistemas de mensajería,  
**QUIERO** implementar un mecanismo de publicación y suscripción basado en Kafka y Redis,  
**PARA** garantizar la distribución eficiente de eventos en tiempo real a múltiples suscriptores.  

## ✅ Criterios de Aceptación

1️⃣ **DADO** que un productor de eventos está en ejecución,  
   **CUANDO** se envíe un mensaje a través del endpoint de publicación,  
   **ENTONCES** el mensaje debe ser enviado al **topic** correspondiente en Kafka.  

2️⃣ **DADO** que hay múltiples suscriptores conectados a Kafka,  
   **CUANDO** un mensaje es publicado en el **topic**,  
   **ENTONCES** cada suscriptor debe recibir una copia del mensaje y procesarlo.  

3️⃣ **DADO** que un suscriptor recibe un evento,  
   **CUANDO** procese el mensaje,  
   **ENTONCES** debe verificar si ya ha sido consumido previamente, evitando duplicados mediante **Redis**.  
