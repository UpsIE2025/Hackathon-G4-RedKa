package com.msc_productor.msc_productor.Controller;

import com.msc_productor.msc_productor.Services.KafkaProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/send")
public class ProductorController {

    private final KafkaProducer kafkaProducer;

    @Autowired
    public ProductorController(KafkaProducer kafkaProducer) {
        this.kafkaProducer = kafkaProducer;
    }

    @PostMapping("/{channel}")
    public ResponseEntity<String> sendMessage(@PathVariable String channel, @RequestBody String data) {
        kafkaProducer.sendData(channel, data);
        return ResponseEntity.ok("Message sent to " + channel);
    }

}
