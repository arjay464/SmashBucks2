import configparser
import balance
import time
import math

config = configparser.ConfigParser()
DailyFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/daily.ini"


async def daily(username: str) -> str:
    config.read(DailyFilePath)
    secs = []
    for sections in config.sections():
        secs.append(sections)
    if username not in secs:
        config.add_section(username)
        config[username]['unix_daily_time'] = "0"
        config[username]['num_uses'] = "0"
        with open(DailyFilePath, "a") as f:
            config.write(f)
    last_daily = config.getfloat(username, 'unix_daily_time')
    num_uses = config.getint(username, "num_uses")
    now = time.gmtime()
    current_time = time.mktime(now)
    if last_daily + 86400 > current_time:
        return "You must wait a full day before claiming daily bonus again."
    else:
        current_balance = await balance.getIntBalance(username)
        daily_amount = (180 / (1 + math.pow(math.e, (float(current_balance) * -0.002)))) - 70
        if daily_amount < 20:
            daily_amount = 20
        elif daily_amount > 60:
            daily_amount = 60

        daily_amount = int(round(daily_amount, 0))

        print(daily_amount)
        output = await balance.botAddBalance(username, daily_amount)
        config[username]['num_uses'] = str(num_uses + 1)
        config[username]['unix_daily_time'] = str(current_time)
        print(username)
        with open(DailyFilePath, 'w') as f:
            config.write(f)
        return output
