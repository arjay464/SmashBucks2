import configparser
import asyncio
import threading
import time
import os

PotatoFilePath = f"{os.getcwd()}/files/potato.ini"


class BlinkTimer:

    def __init__(self, start_time, duration, username, smashbucks):
        self._time = start_time
        self._duration = duration
        self._username = username
        self._active = True
        self._smashbucks = smashbucks
        self._config = configparser.ConfigParser()

        self._b_thread = threading.Thread(target=self.start_blink_timer)
        self._b_thread.start()

    async def start_blink_timer(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self)
        loop.close()

    async def blink_clock(self):

        while self._active:

            now = time.gmtime()
            current_time = time.mktime(now)

            if current_time - self._duration < self._start_time:
                self._active = False

            time.sleep(0.5)

        await self._smashbucks.send(f"{self._username} returned to the confines of this dimension.")

        self._config.read(PotatoFilePath)

        self._config.set(self._username, "3", "1")
        self._config.set(self._username, "2", "0")

        with open(PotatoFilePath, "w") as configfile:
            self._config.write(configfile)
        self._config.clear()