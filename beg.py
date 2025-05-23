import configparser
import discord
import time
import balance
import flavor
import random
import os
import math

config = configparser.ConfigParser()
BegFilePath = f"{os.getcwd()}/files/beg.ini"


async def init_user_beg(username: str) -> None:
    config.read(BegFilePath)
    config[username]['unix_beg_time'] = "0"
    config[username]['num_uses'] = "0"


async def beg(message: discord.Message) -> str:
    config.read(BegFilePath)
    secs = []
    for sections in config.sections():
        secs.append(sections)
    username = message.author.name
    if username not in secs:
        config.add_section(username)
        config[username]['unix_beg_time'] = "0"
        config[username]['num_uses'] = "0"
        with open(BegFilePath, "a") as f:
            config.write(f)
    last_beg = config.getfloat(username, 'unix_beg_time')
    num_uses = config.getint(username, "num_uses")
    now = time.gmtime()
    current_time = time.mktime(now)
    config[username]['num_uses'] = str(num_uses + 1)
    config[username]['unix_beg_time'] = str(current_time)
    print(f"{username} has now begged {int(num_uses) + 1} times")
    with open(BegFilePath, 'w') as f:
        config.write(f)
    config.clear()
    if current_time - last_beg > 300:
        if random.randint(1, 100) == 100:
            crit_reward = random.randint(21, 40)
            result = "You've caught me at the right time... Here's "+str(crit_reward)+" Smashbucks"
            output = await balance.botAddBalance(username, int(crit_reward))
            return result + "\n" + output
        else:
            r = random.randint(1, 1000)
            if r > 985:
                reward = random.randint(5, 20)
                result = "You've caught me at the right time... Here's " + str(reward) + " Smashbucks"
                output = await balance.botAddBalance(username, int(reward))
                return result + "\n" + output

            else:
                if username == "thefuckingwarlock":
                    output = await flavor.get_beg_rejections_noah()
                    return output
                elif username == "eaakis":
                    output = await flavor.get_beg_rejections_eli()
                    return output
                else:
                    output = await flavor.get_beg_rejections_general()
                    return output
    minutes = math.floor((current_time - last_beg) % 60)
    seconds = math.floor(current_time)
    z_mod_m = ""
    z_mod_s = ""
    if minutes < 10:
        z_mod_m = "0"
    if seconds < 10:
        z_mod_s = "0"
    return f"Please wait :) ({z_mod_m}{minutes}:{z_mod_s}{seconds} remaining)"






