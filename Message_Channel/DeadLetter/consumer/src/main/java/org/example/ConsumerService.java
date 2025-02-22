package org.example;


import io.quarkus.redis.client.RedisClient;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.inject.Inject;
import org.eclipse.microprofile.context.ManagedExecutor;

import java.util.Arrays;
import java.util.concurrent.TimeUnit;

@ApplicationScoped
public class ConsumerService {

    @Inject
    RedisClient redisClient;

    @Inject
    ManagedExecutor executor;

    private volatile boolean running = true;

    void onStart(@Observes StartupEvent ev) {
        executor.execute(this::consumeMessages);
    }

    private void consumeMessages() {
        while (running) {
            try {
                var result = redisClient.blpop(Arrays.asList("messages", "1"));
                if (result != null && result.size() > 1) {
                    String message = result.get(1).toString();
                    System.out.println("Mensaje recibido: " + message);
                }else {
                    TimeUnit.MILLISECONDS.sleep(100);
                }
            } catch (Exception e) {
                System.err.println("Error al consumir mensaje: " + e.getMessage());
                try {
                    TimeUnit.SECONDS.sleep(5);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
}
