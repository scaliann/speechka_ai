from aiokafka import AIOKafkaProducer

from app.config import settings

producer: AIOKafkaProducer | None = None


async def init_producer():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_host)
    await producer.start()


def get_producer() -> AIOKafkaProducer:
    if producer is None:
        raise RuntimeError("Kafka producer is not initialized")
    return producer
