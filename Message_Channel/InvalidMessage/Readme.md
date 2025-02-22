# Manejo de Mensajes No Válidos en un Sistema de Mensajería

## Historia Técnica

### Historia
COMO administrador del sistema de mensajería  
QUIERO que los mensajes no válidos sean movidos automáticamente a un canal especial  
PARA evitar interrupciones en el procesamiento y facilitar su posterior análisis y corrección.  

### Criterios de Aceptación

1. **Redirección de Mensajes No Válidos**
   - DADO que un mensaje tiene un formato incorrecto o datos incompletos
   - CUANDO un consumidor intenta procesarlo
   - ENTONCES el mensaje debe ser enviado automáticamente al canal `invalid-messages`.

2. **Registro de Errores**
   - DADO que un mensaje es movido al canal de mensajes no válidos
   - CUANDO se detecta un error en su estructura o contenido
   - ENTONCES se debe registrar un log con la causa del error y los detalles del mensaje.

3. **Monitoreo y Alertas**
   - DADO que el canal `invalid-messages` acumula un número anormal de mensajes
   - CUANDO se supera un umbral predefinido
   - ENTONCES se debe generar una alerta para los administradores del sistema.

4. **Reprocesamiento de Mensajes**
   - DADO que un mensaje en el canal `invalid-messages` es corregido manualmente
   - CUANDO un administrador decide reprocesarlo
   - ENTONCES el mensaje debe ser reenviado al canal de procesamiento normal.

5. **Evitar Bloqueos en el Sistema**
   - DADO que un mensaje defectuoso es recibido
   - CUANDO no puede ser procesado correctamente
   - ENTONCES el sistema debe continuar operando sin interrupciones, enviando el mensaje erróneo al canal correspondiente.
  
## Ejecución de Programa
Para ejecutar el programa se deben seguir los diguientes pasos:

### 1. Levantar Redis en Docker con Docker Compose
Ejecutar el siguiente comando para levantar Redis usando Docker Compose:

```bash
docker compose up --build -d
```

### 2. Ejecutar el Script de Python del Producer

Una vez que Redis esté levantado, ejecutar el script del productor:

```bash
python producer.py
```

### 3. Ejecutar el Script de Python del Consumer

Luego, ejecutar el script del consumidor:

```bash
python consumer.py
```

### 4. Ejecutar el Script de Python del Monitoreo

Finalmente, ejecutar el script del monitoreo:

```bash
python consumer.py
```

## 5. Probar la Funcionalidad con Postman

Para probar la funcionalidad, usa Postman con los siguientes parámetros:

- **URL**: `http://localhost:5000/produce`
- **Método**: `POST`
- **Body (JSON)**:

```json
{
   "id": 1,
  "content": "Envío de Mensaje 1"
}
```
