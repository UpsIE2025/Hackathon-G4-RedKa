package com.msc_consumer.msc_consumer.Services;

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

    public boolean isValidChannel(String channel) {
        return redisTemplate.opsForSet().isMember("valid_channels", channel);
    }

    public void addValidChannel(String channel) {
        redisTemplate.opsForSet().add("valid_channels", channel);
    }
}
