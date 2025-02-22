package com.msc_productor.msc_productor.Controller;

import com.msc_productor.msc_productor.Services.KafkaProducer;
import com.msc_productor.msc_productor.Services.RedisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/send")
public class ProductorController {

    private final KafkaTemplate<String, String> kafkaTemplate;
    private final RedisService redisService;

    @Autowired
    public ProductorController(KafkaTemplate<String, String> kafkaTemplate, RedisService redisService) {
        this.kafkaTemplate = kafkaTemplate;
        this.redisService = redisService;
    }

    // Endpoint para enviar mensajes a Kafka
    @PostMapping("/{channel}")
    public ResponseEntity<String> sendToKafka(@PathVariable String channel, @RequestBody String message) {
        // Verificar si el canal es válido
        if (!redisService.isValidChannel(channel)) {
            return ResponseEntity.badRequest().body("Error: Canal no válido");
        }

        // Enviar mensaje a Kafka si el canal es válido
        kafkaTemplate.send(channel, message);

        return ResponseEntity.ok("Mensaje enviado al canal: " + channel);
    }

}
