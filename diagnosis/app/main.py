# app/main.py
import asyncio
import signal
from logging import getLogger, basicConfig, INFO

from app.database.mongo_db import setup_mongodb
from app.kafka.consumers import routes
from app.utils.background import (
    background_task_manager,
)
from app.utils.consumer import consumer

basicConfig(level=INFO)
logger = getLogger(__name__)


async def run_consumers() -> None:
    if not routes:
        logger.warning("No routes found")
    for routing in routes:
        background_task_manager.add_task(consumer(routing))
    logger.info("Consumers scheduled: %s", [r.topic for r in routes])


async def main() -> None:
    await setup_mongodb()
    logger.info("Mongo initialized")

    await run_consumers()
    logger.info("Consumers initialized")

    stop_evt = asyncio.Event()
    loop = asyncio.get_running_loop()

    def _stop(*_):
        loop.call_soon_threadsafe(stop_evt.set)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _stop)
        except Exception:
            pass

    try:
        await stop_evt.wait()
    finally:
        await background_task_manager.stop()
        logger.info("Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
