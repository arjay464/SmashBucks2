import configparser
import os
from blink import BlinkTimer
from mail import Mail
import time
import random
import math

config = configparser.ConfigParser()
PotatoFilePath = f"{os.getcwd()}/files/potato.ini"
InventoryFilePath = f"{os.getcwd()}/files/inventory.ini"


async def summon(username):
    config.read(InventoryFilePath)
    shard = False
    outlet = 0
    for key in config.items(username):
        if key[0] == "122" or key[0] == "1122":
            shard = True
            outlet = int(key[0])

    if not shard:
        return "You must obtain the Shard of Taskmaster to summon the potato."

    config.read(PotatoFilePath)
    if username in config.sections():
        if config.getint(username, "1") == 1:
            return "You may not summon the same potato twice."

    if config.getint("Setup", "active") == 0:
        return "There is no potato to summon."

    if config.getint("Users", username) == 1:
        return "You cannot summon the potato while holding one."

    config.setint('Setup', username, "1")

    for key, value in config.items('Users'):
        if value == "1":
            config.set('Users', key, "0")
            target = key
            break
    else:
        target = "Something went wrong."

    if outlet == 122:
        config.set(username, "1", "1")

    with open(PotatoFilePath, "w") as configfile:
        config.write(configfile)

    config.clear()
    return f"Summoned potato from {target}"


async def blink(username, smashbucks):
    config.read(InventoryFilePath)
    cloak = False
    outlet = 0
    for key in config.items(username):
        if key[0] == "124" or key[0] == "1124":
            cloak = True
            outlet = int(key[0])

    if not cloak:
        return "You must obtain the Rogue's Cloak to blink yourself."

    config.read(PotatoFilePath)
    if username in config.sections():
        if config.getint(username, "2") == 1:
            return "You've already left the confines of this dimension."

    if username in config.sections():
        if config.getint(username, "3") == 1:
            return "You may not blink more than once per potato."

    if config.getint("Setup", "active") == 0:
        return "The cloak did not detect a threat, and thus didn't blink."

    if config.getint("Users", username) == 1:
        return "You cannot blink while holding a potato."

    config.set(username, "2", "1")
    config.set(username, "3", "1")

    with open(PotatoFilePath, "w") as configfile:
        config.write(configfile)

    config.clear()

    now = time.gmtime()
    current_time = time.mktime(now)

    if outlet == 122:
        BlinkTimer(current_time, 1800, username, smashbucks)
    else:
        BlinkTimer(current_time, 3600, username, smashbucks)

    return f"{Username} left the confines of this dimension."


async def split(username):
    config.read(InventoryFilePath)
    box = False
    outlet = 0
    for key in config.items(username):
        if key[0] == "125" or key[0] == "1125":
            box = True
            outlet = int(key[0])

    if not box:
        return "You must obtain Schrödinger's Box to split the potato."

    config.read(PotatoFilePath)
    if username in config.sections():
        if config.getint(username, "4") == 1:
            return "You may not split the potato twice."

    if config.getint("Users", username) == 0:
        return "You cannot summon the potato without holding one."

    open_player = False
    for user in config.items('Users'):
        if user[1] == "0":
            open_player = True

    if not open_player:
        return "There must be someone to give the split potato to."

    pairs = config.getint("Setup", "pairs")
    config.set("Setup", "pairs", str(pairs + 1))

    open_players = []
    for key, value in config.items('Users'):
        if value == "0":
            open_players.append(key)

    target_idx = random.randint(0, len(open_players) - 1)
    target = open_players[target_idx]

    config.set("Users", target, "1")

    if outlet == 125:
        config.set(username, "4", "1")

    with open(PotatoFilePath, "w") as configfile:
        config.write(configfile)

    config.clear()
    return f"Split potato to {target}!"


async def discover(username, lit_potato):
    config.read(InventoryFilePath)
    tome = False
    outlet = 0
    for key in config.items(username):
        if key[0] == "123" or key[0] == "1123":
            tome = True
            outlet = int(key[0])

    if not tome:
        return "You must obtain the Tome of Inquisition before consulting it."

    if username in config.sections():
        if config.getint(username, "6") == 1:
            return "You may not consult the Tome of Inquisition more that once per potato. "

    now = time.gmtime()
    current_time = time.mktime(now)

    start_time = lit_potato.start_time
    duration = current_time - start_time

    if outlet == 1123:
        hours = math.floor(duration / 3600)
        duration = duration % 3600
        minutes = math.floor(duration / 60)
        seconds = int(duration % 60)
        z_mod_h = ""
        z_mod_m = ""
        z_mod_s = ""
        if hours < 10:
            z_mod_h = "0"
        if minutes < 10:
            z_mod_m = "0"
        if seconds < 10:
            z_mod_s = "0"
        t = f"The potato will detonate in approximately {z_mod_h}{hours}:{z_mod_m}{minutes}:{z_mod_s}{seconds}.", 1

    else:
        true_lower = int(duration) * 0.9
        true_higher = int(duration) * 1.1
        lower_buffer = round(random.uniform(-0.08, 0.35), 3)
        higher_buffer = round(random.uniform(-0.08, 0.35), 3)

        display_lower = true_lower - (lower_buffer * int(duration))
        display_higher = true_higher + (higher_buffer * int(duration))

        t = f"The Ancient Wisdom predicts a detonation between {convert_time(display_lower)} and {convert_time(display_higher)} from now."

    config.set(username, "6", "1")

    with open(PotatoFilePath, "w") as configfile:
        config.write(configfile)

    config.clear()
    return t


async def blackmail(username, smashbucks, lit_potato):
    config.read(InventoryFilePath)
    mail = False
    outlet = 0
    for key in config.items(username):
        if key[0] == "126" or key[0] == "1126":
            mail = True
            outlet = int(key[0])

    if not mail:
        return "You cannot need the Blackmail Letter to, well, blackmail someone."

    if username in config.sections():
        if config.getint(username, "5") == 1:
            return "You don't have enough gossip to blackmail twice per potato."

    if config.getint("Setup", "active") == 0:
        return "There's no sense in blackmailing someone without an active potato."

    target = lit_potato.owner
    if outlet == 1126:
        config.set(target, "7", "1")
        Mail(target, smashbucks)
        t = f"{target} has been critically blackmailed by {username}!"
    else:
        Mail(target, smashbucks)
        t = f"{target} has been blackmailed by {username}!"

    config.set(username, "5", "1")

    with open(PotatoFilePath, "w") as configfile:
        config.write(configfile)

    config.clear()

    return t
