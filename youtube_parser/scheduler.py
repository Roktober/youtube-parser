import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:
    def __init__(self):
        self._scheduler = AsyncIOScheduler(event_loop=asyncio.get_running_loop())

    def add_job(self, **kwargs) -> None:
        self._scheduler.add_job(**kwargs)

    def start(self):
        self._scheduler.start()

    def stop(self) -> None:
        self._scheduler.shutdown()
