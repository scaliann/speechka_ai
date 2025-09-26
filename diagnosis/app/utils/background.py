# app/utils/background.py
import asyncio
from collections.abc import Awaitable
from logging import getLogger

logger = getLogger(__name__)


class BackgroundTaskManager:
    """Schedules background tasks in the CURRENT running loop."""

    def __init__(self) -> None:
        self._tasks: set[asyncio.Task] = set()

    def add_task(self, aw: Awaitable) -> asyncio.Task:
        task = asyncio.get_running_loop().create_task(aw)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        logger.info(
            "added background task: %s",
            getattr(aw, "__name__", aw),
            extra={"tasks_count": len(self._tasks)},
        )
        return task

    async def stop(self) -> None:
        if not self._tasks:
            return
        for t in list(self._tasks):
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        logger.info("background tasks stopped", extra={"tasks_count": 0})


background_task_manager = BackgroundTaskManager()
