import configparser
import discord
import time
import random
import os

config = configparser.ConfigParser()
CardFilePath = f"{os.getcwd()}/files/cards.ini"
PowerFilePath = f"{os.getcwd()}/files/power.ini"
ClientListFilePath = f"{os.getcwd()}/files/client_list.ini"
DisplayNameFilePath = f"{os.getcwd()}/files/display_names.ini"


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
    elif card_id < 128:
        card_file = config.get("Artifact", str(card_id))
        card_file = "/Artifact/" + card_file
    elif card_id < 1035:
        card_file = config.get("Holo_Common", str(card_id))
        card_file = "/Common_h/" + card_file
    elif card_id < 1067:
        card_file = config.get("Holo_Uncommon", str(card_id))
        card_file = "/Uncommon_h/" + card_file
    elif card_id < 1092:
        card_file = config.get("Holo_Rare", str(card_id))
        card_file = "/Rare_h/" + card_file
    elif card_id < 1104:
        card_file = config.get("Holo_Epic", str(card_id))
        card_file = "/Epic_h/" + card_file
    elif card_id < 1119:
        card_file = config.get("Holo_Ultimate", str(card_id))
        card_file = "/Ultimate_h/" + card_file
    elif card_id < 1122:
        card_file = config.get("Holo_Mythic", str(card_id))
        card_file = "/Mythic_h/" + card_file
    elif card_id < 1128:
        card_file = config.get("Holo_Artifact", str(card_id))
        card_file = "/Artifact_h/" + card_file
    else:
        card_file = "INVALID"

    card_file = f"{os.getcwd()}/SmashBucksCards"+card_file+".png"
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
    elif card_id < 128:
        card_file = config.get("Artifact", str(card_id))
    elif card_id < 1035:
        card_file = config.get("Holo_Common", str(card_id))
    elif card_id < 1067:
        card_file = config.get("Holo_Uncommon", str(card_id))
    elif card_id < 1092:
        card_file = config.get("Holo_Rare", str(card_id))
    elif card_id < 1104:
        card_file = config.get("Holo_Epic", str(card_id))
    elif card_id < 1119:
        card_file = config.get("Holo_Ultimate", str(card_id))
    elif card_id < 1122:
        card_file = config.get("Holo_Mythic", str(card_id))
    elif card_id < 1128:
        card_file = config.get("Holo_Artifact", str(card_id))
    else:
        return
    return card_file


async def card_shuffler(username="None") -> int:
    time.sleep(0.5)
    roll = random.randint(1, 1006)
    h_roll = random.randint(1, 150)
    print(f"Gacha @{username} [{roll}]")
    if h_roll == 150:
        roll += 1000
    if roll == 2000:
        return random.randint(1119, 1121)
    if roll > 2000:
        return random.randint(1122, 1126)
    if roll > 1990:
        return random.randint(1104, 1118)
    if roll > 1970:
        return random.randint(1092, 1103)
    if roll > 1900:
        return random.randint(1067, 1091)
    if roll > 1700:
        return random.randint(1035, 1066)
    if roll > 1006:
        return random.randint(1001, 1034)
    if roll > 1000:
        return random.randint(122, 126)
    if roll == 1000:
        return random.randint(119, 121)
    if roll > 990:
        return random.randint(104, 118)
    if roll > 970:
        return random.randint(92, 103)
    if roll > 900:
        return random.randint(67, 91)
    if roll > 700:
        return random.randint(35, 66)
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

    for key, value in config.items("Artifact"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Common"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Uncommon"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Rare"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Epic"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Ultimate"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Mythic"):
        if value == name:
            return int(key)

    for key, value in config.items("Holo_Artifact"):
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
    elif card_id < 128:
        return "Artifact"
    if card_id < 1035:
        return "Holo_Common"
    elif card_id < 1067:
        return "Holo_Uncommon"
    elif card_id < 1092:
        return "Holo_Rare"
    elif card_id < 1104:
        return "Holo_Epic"
    elif card_id < 1119:
        return "Holo_Ultimate"
    elif card_id < 1122:
        return "Holo_Mythic"
    elif card_id < 1128:
        return "Holo_Artifact"
    else:
        return "Invalid ID"


async def get_card_power(name: str) -> int:
    config.read(PowerFilePath)
    card_id = await name_to_id(name)
    return config.getint("Cards", str(card_id))


def sort(e: tuple) -> int:
    return e[0]


async def normalize_card_name(name: str) -> str:
    s = ""
    for char in name:
        if 96 < ord(char) < 123:
            s += char
    if s == "rosalinaandluma":
        return "rosalinaluma"

    if s == "mrgameandwatch":
        return "mrgamewatch"

    if s == "banjoandkazooie":
        return "banjokazooie"

    if s == "pyraandmythra":
        return "pyramythra"

    if s == "schrdingersbox":
        return "schrodingersbox"

    return s


async def get_inventory_display_name(card_id: int) -> str:
    config.read(DisplayNameFilePath)
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
    elif card_id < 128:
        card_file = config.get("Artifact", str(card_id))
    elif card_id < 1035:
        card_file = config.get("Holo_Common", str(card_id))
    elif card_id < 1067:
        card_file = config.get("Holo_Uncommon", str(card_id))
    elif card_id < 1092:
        card_file = config.get("Holo_Rare", str(card_id))
    elif card_id < 1104:
        card_file = config.get("Holo_Epic", str(card_id))
    elif card_id < 1119:
        card_file = config.get("Holo_Ultimate", str(card_id))
    elif card_id < 1122:
        card_file = config.get("Holo_Mythic", str(card_id))
    elif card_id < 1128:
        card_file = config.get("Holo_Artifact", str(card_id))
    else:
        card_file = "Card Not Found"
    return card_file
