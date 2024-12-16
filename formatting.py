import configparser
import discord
import time
import random

config = configparser.ConfigParser()
CardFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/cards.ini"
PowerFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/power.ini"
ClientListFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/client_list.ini"


async def formatId(id_reference: str) -> str:
    id_reference = id_reference[2:-1]
    config.read(ClientListFilePath)
    for key, value in config.items('client_list'):
        if value == id_reference:
            return key


async def display_card(card_id: int) -> str:
    config.read(CardFilePath)
    if card_id < 35:
        card_file = config.get("Common", str(card_id))
        card_file = "/Common/" + card_file
    elif card_id < 67:
        card_file = config.get("Uncommon", str(card_id))
        card_file = "/Uncommon/" + card_file
    elif card_id < 92:
        card_file = config.get("Rare", str(card_id))
        card_file = "/Rare/" + card_file
    elif card_id < 104:
        card_file = config.get("Epic", str(card_id))
        card_file = "/Epic/" + card_file
    elif card_id < 119:
        card_file = config.get("Ultimate", str(card_id))
        card_file = "/Ultimate/" + card_file
    elif card_id < 122:
        card_file = config.get("Mythic", str(card_id))
        card_file = "/Mythic/" + card_file
    elif card_id < 125:
        card_file = config.get("Artifact", str(card_id))
        card_file = "/Artifact/" + card_file
    else:
        card_file = "INVALID"

    card_file = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/SmashBucksCards"+card_file+".png"
    return card_file


async def output_card(card_file: str, channel: discord.PartialMessageable) -> None:
    card = discord.File(card_file)
    await channel.send(file=card)


async def get_card_name(card_id: int) -> str:
    config.read(CardFilePath)
    if card_id < 35:
        card_file = config.get("Common", str(card_id))
    elif card_id < 67:
        card_file = config.get("Uncommon", str(card_id))
    elif card_id < 92:
        card_file = config.get("Rare", str(card_id))
    elif card_id < 104:
        card_file = config.get("Epic", str(card_id))
    elif card_id < 119:
        card_file = config.get("Ultimate", str(card_id))
    elif card_id < 122:
        card_file = config.get("Mythic", str(card_id))
    elif card_id < 125:
        card_file = config.get("Artifact", str(card_id))
    else:
        return
    return card_file


async def card_shuffler() -> int:
    time.sleep(4)
    roll = random.randint(1, 1000)
    print(roll)
    if roll == 1000:
        return random.randint(119, 121)
    elif roll > 990:
        return random.randint(104, 118)
    elif roll > 970:
        return random.randint(92, 103)
    elif roll > 900:
        return random.randint(67, 91)
    elif roll > 700:
        return random.randint(35, 66)
    else:
        return random.randint(1, 34)


async def name_to_id(name: str) -> int:
    config.read(CardFilePath)
    for key, value in config.items("Common"):
        if value == name:
            return int(key)
    for key, value in config.items("Uncommon"):
        if value == name:
            return int(key)

    for key, value in config.items("Rare"):
        if value == name:
            return int(key)

    for key, value in config.items("Epic"):
        if value == name:
            return int(key)

    for key, value in config.items("Ultimate"):
        if value == name:
            return int(key)

    for key, value in config.items("Mythic"):
        if value == name:
            return int(key)

    for key,value in config.items("Artifact"):
        if value == name:
            return int(key)
    return -1


async def get_card_type(card_id: int) -> str:
    config.read(CardFilePath)
    if card_id < 35:
        return "Common"
    elif card_id < 67:
        return "Uncommon"
    elif card_id < 92:
        return "Rare"
    elif card_id < 104:
        return "Epic"
    elif card_id < 119:
        return "Ultimate"
    elif card_id < 122:
        return "Mythic"
    elif card_id < 125:
        return "Artifact"
    else:
        return


async def get_card_power(name: str) -> int:
    config.read(PowerFilePath)
    return config.getint("Cards", name)


def sort(e: tuple) -> int:
    return e[0]










