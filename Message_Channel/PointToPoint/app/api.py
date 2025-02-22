import json
from typing import List

from fastapi import FastAPI
from kafka import KafkaProducer
from pydantic import BaseModel
from starlette.exceptions import HTTPException

app = FastAPI()

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = 'point_to_point'
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)


class Message(BaseModel):
    value: dict


@app.post("/send-message/")
async def send_message(messages: List[Message]):
    try:
        for message in messages:
            value = json.dumps(message.value).encode('utf-8')
            producer.send('point_to_point', value)
        return {"message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
