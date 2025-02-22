package com.msc_productor.msc_productor.Services;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

@Service
public class RedisService {
    private final RedisTemplate<String, String> redisTemplate;

    @Autowired
    public RedisService(RedisTemplate<String, String> redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    // Método para validar si un canal es válido
    public boolean isValidChannel(String channel) {
        // Revisar si el canal existe en el conjunto de canales válidos en Redis
        return redisTemplate.opsForSet().isMember("valid_channels", channel);
    }
}
