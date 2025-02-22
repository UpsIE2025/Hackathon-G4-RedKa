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
                // Leer un mensaje de la lista de fallos
                var result = redisClient.blpop(Arrays.asList("failedMessages", "1"));
                if (result != null && result.size() > 1) {
                    String failureDetails = result.get(1).toString();
                    System.out.println("Mensaje fallido recibido: " + failureDetails);

                    // Procesar el fallo
                    // Aquí es donde puedes realizar un procesamiento adicional si es necesario
                    processFailureDetails(failureDetails);
                } else {
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

    private void processFailureDetails(String failureDetails) {
        // Almacenar detalles adicionales si es necesario, por ejemplo en otra lista o base de datos
        // Aquí se podrían almacenar las estadísticas en tiempo real o cualquier otro dato relevante.
        System.out.println("Procesando detalles de fallo: " + failureDetails);
        redisClient.rpush(java.util.Arrays.asList("processedFailedMessages", failureDetails));
    }
}

