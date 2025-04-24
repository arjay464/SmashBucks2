import asyncio
import threading
import time
import configparser
import os

PotatoFilePath = f"{os.getcwd()}/files/potato.ini"


class Mail:

    def __init__(self, target, smashbucks):
        self._duration = 6000
        self._active = True
        self._target = target

        now = time.gmtime()
        current_time = time.mktime(now)

        self._start_time = current_time

        self._smashbucks = smashbucks

        self._config = configparser.ConfigParser()
        self._config.read(PotatoFilePath)

        self._config.set(self._target, "8", "1")

        with open(PotatoFilePath, "w") as configfile:
            self._config.write(configfile)

        self._m_thread = threading.Thread(target=self.mail_clock_start)
        self._m_thread.start()

    def mail_clock_start(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.mail_clock)
        loop.close()

    async def mail_clock(self):
        while self._active:
            now = time.gmtime()
            current_time = time.mktime(now)

            if current_time - self._duration < self._start_time:
                self._active = False

            time.sleep(0.5)

        await smashbucks.send(f"{self._target} has recovered from their blackmailing.")

        self._config.read(PotatoFilePath)

        self._config.set(self._target, "8", "0")

        with open(PotatoFilePath, "w") as configfile:
            self._config.write(configfile)
        self._config.clear()


