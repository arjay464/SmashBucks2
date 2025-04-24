import configparser
import discord
import math
import os
import asyncio
import threading
import time
import random
import balance

PotatoFilePath = f"{os.getcwd()}/files/potato.ini"
config = configparser.ConfigParser()


class Potato:

    def __init__(self, username, smashbucks, damage, fuse=None):
        if fuse is None:
            self.fuse = random.randint(10800, 21600)
        else:
            self.fuse = fuse
        self._owner = username
        self._damage = damage
        self._active = False
        self._smashbucks = smashbucks
        self._config = configparser.ConfigParser()

        self._config.read(PotatoFilePath)
        self._config.set('Setup', 'active', "1")
        self._config.set('Users', username, "1")

        with open(PotatoFilePath, 'w') as f:
            self._config.write(f)
        self._config.clear()

        now = time.gmtime()
        current_time = time.mktime(now)
        self._end = int(current_time + self.fuse)
        self._start_time = current_time

        self._p_thread = threading.Thread(target=self.start_potato_loop)
        self._p_thread.start()

    @property
    def p_thread(self):
        return self._p_thread

    @property
    def start_time(self):
        return self._start_time

    @property
    def owner(self):
        return self._owner

    def start_potato_loop(self):
        self._active = True
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.potato_clock())
        loop.close()

    async def potato_clock_stop(self):
        now = time.gmtime()
        current_time = time.mktime(now)
        if current_time > self._end:
            self._active = False
        else:
            self._active = True

    async def potato_clock(self):
        while self._active:
            await self.potato_clock_stop()
            time.sleep(0.5)

        self._config.read(PotatoFilePath)
        num_users = self._config.getint('Setup', 'num_users')

        holders = []
        for key, value in self._config.items('Users'):
            if value == "1":
                holders.append(key)

        r_idx = random.randint(0, len(holders) - 1)
        self._owner = holders[r_idx]

        c_bal = await balance.userBalance(self._owner)
        output1 = await balance.botSubBalance(self._owner, c_bal - damage)

        if num_users == 1:
            payout = damage // num_users
        else:
            payout = damage // (num_users - 1)

        await self._smashbucks.send(f"BOOOOOM!\nThe Hot Potato exploded while {self._owner} was holding it!\n{output1}")

        for key, value in self._config.items('Users'):
            if not key == self._owner:
                output = await balance.botAddBalance(key, payout)
                await self._smashbucks.send(output)

        now = time.gmtime()
        current_time = time.mktime(now)

        self._config.set('Setup', 'lockout', str(current_time + 18000))
        self._config.set('Setup', 'active', "0")

        for item in self._config.items('Users'):
            self._config.set('Users', item[0], "0")

        for section in self._config.sections():
            for key, value in self._config.items(section):
                self._config.set(section, key, "0")

        with open(PotatoFilePath, 'w') as configfile:
            self._config.write(configfile)
        self._config.clear()

    async def pass_potato(self, target: str, username: str):
        self._config.read(PotatoFilePath)
        self._config.set('Users', username, "0")
        self._config.set('Users', target, "1")
        with open(PotatoFilePath, 'w') as configfile:
            self._config.write(configfile)
        self._config.clear()
        self._owner = target
        return f"{username} passed the potato to {target}"


async def potato_opt_in(username: str) -> str:
    config.read(PotatoFilePath)

    config.set('Users', username, str(0))
    n = config.getint('Setup', 'num_users')

    config.set('Setup', 'num_users', str(n + 1))

    config.add_section(username)
    for i in range(1, 9):
        config.set(username, str(i), "0")

    with open(PotatoFilePath, 'w') as configfile:
        config.write(configfile)

    config.clear()
    return f"{username} is now accepting Hot Potatoes."


async def potato_opt_out(username: str) -> str:
    config.read(PotatoFilePath)

    config.remove_option('Users', username)
    n = config.getint('Setup', 'num_users')

    config.set('Setup', 'num_users', str(n - 1))

    config.remove_section(username)

    with open(PotatoFilePath, 'w') as configfile:
        config.write(configfile)

    config.clear()
    return f"{username} is no longer accepting Hot Potatoes."
