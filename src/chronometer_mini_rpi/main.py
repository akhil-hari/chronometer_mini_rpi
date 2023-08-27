# import subprocess
# subprocess.run(["poetry","show"])

import asyncio

from chronometer_mini_rpi.scheduler.handler import schedule_handler
from chronometer_mini_rpi.scheduler.runtime import run_loop

if __name__ == "__main__":
    asyncio.run(run_loop(schedule_handler))
