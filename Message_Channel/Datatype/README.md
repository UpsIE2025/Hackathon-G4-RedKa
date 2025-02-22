# Historia de Usuario Técnica

## Título: Implementación de canales de mensajes separados por tipo de datos en una institución financiera

**Como** desarrollador del sistema de mensajería de la institución financiera,  
**Quiero** que cada tipo de datos financieros se envíe a través de un canal específico,  
**Para que** el remitente y el receptor puedan identificar y procesar los datos de manera eficiente y segura.

---

### Criterios de aceptación:

#### Canales separados por tipo de datos:
- Debe existir un canal dedicado para cada tipo de datos financieros (por ejemplo, `transacciones`, `alertas_fraude`, `notificaciones_clientes`).
- Cada canal solo debe contener datos del tipo correspondiente.

#### Selección del canal por el remitente:
- El remitente debe poder identificar el tipo de datos que está enviando.
- El remitente debe seleccionar automáticamente el canal correcto basado en el tipo de datos.
  
  **Ejemplo:** Si el remitente envía una transacción, debe usar el canal `transacciones`.

#### Recepción y procesamiento por el receptor:
- El receptor debe saber de qué tipo son los datos basándose en el canal del que se recibieron.
- El receptor debe procesar los datos según su tipo sin necesidad de validaciones adicionales.

  **Ejemplo:** Si los datos se reciben en el canal `alertas_fraude`, el receptor asume que son alertas y las procesa como tal.

#### Ejemplo de flujo de trabajo:
1. Un cliente realiza una transacción con su tarjeta de débito.
2. El sistema identifica que es un dato de tipo `transacciones` y lo envía al canal `transacciones`.
3. El servidor recibe los datos en el canal `transacciones` y los procesa para actualizar el saldo de la cuenta del cliente.

#### Validación de integridad:
- Si un dato se envía a un canal incorrecto, el sistema debe rechazarlo y notificar al remitente.

  **Ejemplo:** Si un dato de tipo `notificaciones_clientes` se envía al canal `alertas_fraude`, el sistema debe generar un error.
