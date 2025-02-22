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
            redisClient.rpush(java.util.Arrays.asList("messages", message));
            return "Mensaje publicado en Redis: " + message;
        } catch (Exception e) {
            return "Error al publicar mensaje: " + e.getMessage();
        }
    }
}
