package com.msc_consumer.msc_consumer.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.stereotype.Service;

@Service
@EnableKafka
public class KafkaConsumer {

    private final RedisService redisService;

    @Autowired
    public KafkaConsumer(RedisService redisService) {
        this.redisService = redisService;
    }

    @KafkaListener(topics = "transacciones", groupId = "group_id")
    public void consumeTransaction(String message) {
        if (redisService.isValidChannel("transacciones")) {
            System.out.println("Received transaction: " + message);
            // Lógica para procesar la transacción
        } else {
            System.out.println("Invalid channel for transacciones");
        }
    }

    @KafkaListener(topics = "alertas_fraude", groupId = "group_id")
    public void consumeAlert(String message) {
        if (redisService.isValidChannel("alertas_fraude")) {
            System.out.println("Received alert: " + message);
            // Lógica para procesar alerta de fraude
        } else {
            System.out.println("Invalid channel for alertas_fraude");
        }
    }

    @KafkaListener(topics = "notificaciones_clientes", groupId = "group_id")
    public void consumeNotification(String message) {
        if (redisService.isValidChannel("notificaciones_clientes")) {
            System.out.println("Received notification: " + message);
            // Lógica para procesar notificación
        } else {
            System.out.println("Invalid channel for notificaciones_clientes");
        }
    }
}
