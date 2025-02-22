# Historia de Usuario: Message Channel / Point-to-Point

**Como** sistema de procesamiento de transacciones  
**Quiero** enviar mensajes a través de un canal punto a punto  
**Para** garantizar que cada mensaje sea procesado por un único consumidor

---

## 🎯 Criterios de Aceptación

1. **Exclusividad en la Entrega**
   - Un mensaje enviado al canal debe ser recibido por exactamente un receptor
   - Con 3+ receptores activos, el canal selecciona uno por mensaje

2. **Manejo de Concurrencia**
   - Bloqueo de mensaje tras consumo exitoso
   - Notificación de fallo para receptores no seleccionados

3. **Procesamiento Paralelo**
   - Múltiples receptores deben poder consumir mensajes diferentes simultáneamente
   - Ejemplo: 5 mensajes + 3 receptores → 5 mensajes procesados sin solapamientos