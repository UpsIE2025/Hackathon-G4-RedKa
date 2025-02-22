package org.example;

import io.quarkus.redis.client.RedisClient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;

@Path("/producer")
@ApplicationScoped
public class ProducerResource {

    @Inject
    RedisClient redisClient;

    @POST
    @Path("/publish/{message}")
    @Produces(MediaType.TEXT_PLAIN)
    public String publishMessage(@PathParam("message") String message) {
        try {
            // Simulación de un fallo en el envío
            boolean deliverySuccess = simulateMessageFailure(message);

            if (!deliverySuccess) {
                // Se almacena el mensaje fallido
                String failureDetails = createFailureDetails(message, "Error al entregar", "SMS");
                redisClient.rpush(java.util.Arrays.asList("failedMessages", message));// Redis list to store failed messages
                return "Mensaje fallido almacenado en Redis: " + message;
            }

            redisClient.rpush(java.util.Arrays.asList("messages", message));
            return "Mensaje publicado en Redis: " + message;

        } catch (Exception e) {
            return "Error al publicar mensaje: " + e.getMessage();
        }
    }

    private boolean simulateMessageFailure(String message) {
        // Simulamos un fallo en la entrega
        return message.contains("fail");
    }

    private String createFailureDetails(String message, String error, String channel) {
        // Detalles del fallo en formato JSON
        return String.format("{\"message\": \"%s\", \"error\": \"%s\", \"channel\": \"%s\"}", message, error, channel);
    }
}

