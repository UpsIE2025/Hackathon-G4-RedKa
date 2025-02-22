package org.example;

import io.vertx.redis.client.Command;
import io.vertx.redis.client.Request;
import io.vertx.redis.client.impl.RedisClient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionStage;

//@Path("/monitoring")
//@ApplicationScoped
public class MonitoringResource {

    @Inject
    RedisClient redisClient;

    /*@GET
    @Path("/failed-message-count")
    @Produces(MediaType.APPLICATION_JSON)
    public CompletionStage<Response> getFailedMessageCount() {
        CompletableFuture<Response> future = new CompletableFuture<>();

        redisClient.send(Request.cmd(Command.LLEN, "failedMessages"))
                .onSuccess(response -> {
                    Long failedCount = response.toLong();
                    future.complete(Response.ok("{\"failedMessages\": " + failedCount + "}").build());
                })
                .onFailure(err -> {
                    future.complete(Response.status(Response.Status.INTERNAL_SERVER_ERROR)
                            .entity("{\"error\": \"Error al obtener estadísticas: " + err.getMessage() + "\"}")
                            .build());
                });

        return future;
    }*/
}
