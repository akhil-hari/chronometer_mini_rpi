from datetime import timedelta
from asyncio import sleep
from typing import Callable

from scheduler import Scheduler

async def run_loop(handle: Callable):
    
    scheduler = Scheduler()
    scheduler.cyclic(timedelta(seconds=60), handle=handle)
    while True:
        scheduler.exec_jobs()
        await sleep(0.1)
