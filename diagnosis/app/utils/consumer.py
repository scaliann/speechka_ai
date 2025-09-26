from __future__ import annotations
from asyncio import sleep
from collections.abc import Callable, Coroutine
from inspect import signature
from logging import getLogger
from typing import Any

from aiokafka import AIOKafkaConsumer
from pydantic import BaseModel

from app.config import settings

logger = getLogger(__name__)


class RoutingData(BaseModel):
    topic: str
    group_id: str
    handler: Callable[..., Coroutine[Any, Any, None]]
    auto_offset_reset: str = "earliest"
    isolation_level: str = "read_uncommitted"
    enable_auto_commit: bool = False


async def consumer(routing_data: RoutingData):
    sig = signature(routing_data.handler)
    data_class: type[BaseModel] = sig.parameters["data"].annotation

    logger.info(f"Start consuming from {routing_data.topic}")

    while True:
        try:
            consumer = AIOKafkaConsumer(
                routing_data.topic,
                bootstrap_servers=settings.kafka_host,
                group_id=routing_data.group_id,
                auto_offset_reset=routing_data.auto_offset_reset,
                isolation_level=routing_data.isolation_level,
                enable_auto_commit=routing_data.enable_auto_commit,
            )
            await consumer.start()
            try:
                async for msg in consumer:
                    raw = (
                        msg.value.decode("utf-8")
                        if isinstance(msg.value, (bytes, bytearray))
                        else str(msg.value)
                    )
                    logger.info(
                        f"Consume message from topic={routing_data.topic} partition{msg.partition} offset={msg.offset}",
                        extra={
                            "data": raw,
                        },
                    )

                    data = data_class.model_validate_json(raw)

                    try:
                        await routing_data.handler(data)
                        if not routing_data.enable_auto_commit:
                            await consumer.commit()
                    except Exception as handler_ex:
                        logger.error(
                            f"Handler error (topic={routing_data.topic}, partition={msg.partition}, offset={msg.offset})",
                            exc_info=handler_ex,
                        )
            finally:
                await consumer.stop()

        except Exception as ex:
            logger.error(
                f"Error in Kafka consuming: topic={routing_data.topic} group={(routing_data.group_id,)}",
                exc_info=ex,
            )
            await sleep(5)
