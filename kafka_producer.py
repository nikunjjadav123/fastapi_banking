from kafka import KafkaProducer
import json
from .config import settings

producer = KafkaProducer(
    bootstrap_servers=[settings.kafka_broker],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_event(topic: str, event: dict):
    producer.send(topic, event)
    producer.flush()
