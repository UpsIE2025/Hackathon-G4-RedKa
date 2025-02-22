package com.msc_consumer.msc_consumer.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class RedisChannelInitializer implements CommandLineRunner {
    private final RedisService redisService;

    @Autowired
    public RedisChannelInitializer(RedisService redisService) {
        this.redisService = redisService;
    }

    @Override
    public void run(String... args) throws Exception {
        // Inicializar los canales válidos en Redis
        redisService.addValidChannel("transacciones");
        redisService.addValidChannel("alertas_fraude");
        redisService.addValidChannel("notificaciones_clientes");

        System.out.println("Channels initialized in Redis.");
    }
}
