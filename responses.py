import re
import time
import os
import balance
import formatting
import flavor
import beg
import configparser
import daily
import potato
import math
import game_actions
from mail import Mail

config = configparser.ConfigParser()
InventoryFilePath = f"{os.getcwd()}/files/inventory.ini"
PuzzleFilePath = f"{os.getcwd()}/files/puzzle.ini"
mapFilePath = f"{os.getcwd()}/map/map.png"
PotatoFilePath = f"{os.getcwd()}/files/potato.ini"
InitFilePath = f"{os.getcwd()}/files/init.ini"
lit_potato = None

async def handleResponse(message, smashbucks):
    global lit_potato
    text = message.content
    username = message.author.name
    id = message.author.id

    if re.search("%give*", text):
        text = text.replace("%give ", "")
        idx = text.find(" ")
        if idx == -1:
            return "%give requires a space between the subject and amount\nex: %give @arjay 50"
        username = await formatting.formatId(text[:idx])
        amount = int(text[idx+1:])
        output = await balance.addBalance(username, amount, message.author.name)
        return output

    if re.search("%revoke*", text):
        text = text.replace("%revoke ", "")
        idx = text.find(" ")
        if idx == -1:
            return "%revoke requires a space between the subject and amount\nex: %revoke @arjay 50"
        username = await formatting.formatId(text[:idx])
        amount = int(text[idx+1:])
        output = await balance.subBalance(username, amount, message.author.name)
        return output

    if text == "%beg":
        output = await beg.beg(message)
        return output

    if text == "%balance":
        output = await balance.getBalance(message.author.name)
        return output

    if text == "%help":
        return "https://docs.google.com/document/d/1PjgFQvvWEgWCSmILofrdzbbeOGSSzPWwJpwN-huRIHk/edit?usp=sharing"

    if text == "%random_card":
        if username == "arjay_tg" or username == "_camden":
            card_id = await formatting.card_shuffler(username)
            file_path = await formatting.display_card(card_id)
            await formatting.output_card(file_path, message.channel)
            return
        else:
            return "Access Denied."

    if text == "%gacha":
        current_balance = await balance.userBalance(message.author.name)
        if current_balance >= 20:
            card_id = await formatting.card_shuffler(username)
            file_path = await formatting.display_card(card_id)
            await formatting.output_card(file_path, message.channel)
            config.read(InventoryFilePath)
            cards = []
            for key, value in config.items(username):
                cards.append(key)
            if str(card_id) in cards:
                config[username][str(card_id)] = str(config.getint(username, str(card_id)) + 1)
            else:
                config[username][str(card_id)] = "1"
            with open(InventoryFilePath, "w") as configfile:
                config.write(configfile)
            config.clear()
            output = await balance.botSubBalance(message.author.name, 20)
            return output
        else:
            return "Insufficient Funds"

    if text == "%inventory":
        config.read(InventoryFilePath)
        cards = []
        for key, value in config.items(username):
            name = await formatting.get_inventory_display_name(int(key))
            if int(value) > 1:
                cards.append(name + " x"+value)
            else:
                cards.append(name)
        output = "\n".join(cards)
        config.clear()
        return f"{message.author.name}'s Inventory:\n"+output

    if re.search("%sell*", text):
        text.replace("'", "_")
        text = text.replace("%sell ", "")
        text = text.lower()
        text = await formatting.normalize_card_name(text)
        card_id = await formatting.name_to_id(text)
        config.read(InventoryFilePath)
        try:
            x = config.getint(username, str(card_id))
            if x > 1:
                config[username][str(card_id)] = str(config.getint(username, str(card_id)) - 1)
            else:
                config.remove_option(username, str(card_id))
            with open(InventoryFilePath, "w") as configfile:
                config.write(configfile)
            config.clear()
        except Exception as e:
            print(e)
            return "Card not found in inventory."
        card_rarity = await formatting.get_card_type(card_id)
        if card_rarity == "Common":
            output = await balance.botAddBalance(message.author.name, 7)
            return output
        elif card_rarity == "Uncommon":
            output = await balance.botAddBalance(message.author.name, 18)
            return output
        elif card_rarity == "Rare":
            output = await balance.botAddBalance(message.author.name, 40)
            return output
        elif card_rarity == "Epic":
            output = await balance.botAddBalance(message.author.name, 100)
            return output
        elif card_rarity == "Ultimate":
            output = await balance.botAddBalance(message.author.name, 250)
            return output
        elif card_rarity == "Mythic":
            output = await balance.botAddBalance(message.author.name, 1000)
            return output
        elif card_rarity == "Artifact":
            output = await balance.botAddBalance(message.author.name, 750)
            return output
        elif card_rarity == "Holo_Common":
            output = await balance.botAddBalance(message.author.name, 28)
            return output
        elif card_rarity == "Holo_Uncommon":
            output = await balance.botAddBalance(message.author.name, 72)
            return output
        elif card_rarity == "Holo_Rare":
            output = await balance.botAddBalance(message.author.name, 160)
            return output
        elif card_rarity == "Holo_Epic":
            output = await balance.botAddBalance(message.author.name, 400)
            return output
        elif card_rarity == "Holo_Ultimate":
            output = await balance.botAddBalance(message.author.name, 1000)
            return output
        elif card_rarity == "Holo_Mythic":
            output = await balance.botAddBalance(message.author.name, 4000)
            return output
        elif card_rarity == "Holo_Artifact":
            output = await balance.botAddBalance(message.author.name, 3000)
            return output

    if text == "%prices":
        return "COMMON: 7 Smashbucks\nUNCOMMON: 18 Smashbucks\nRARE: 40 Smashbucks\nEPIC: 100 Smashbucks\nULTIMATE: 250 Smashbucks\nARTIFCAT: 750 Smashbucks\nMYTHIC: 1000 Smashbucks\nHOLO x4"

    if re.search("%view*", text):
        text.replace("'", "_")
        text = text.replace("%view ", "")
        text = text.lower()
        text = await formatting.normalize_card_name(text)
        card_id = await formatting.name_to_id(text)
        config.read(InventoryFilePath)
        try:
            x = config.get(username, str(card_id))
            file_path = await formatting.display_card(card_id)
            await formatting.output_card(file_path, message.channel)
            config.clear()
        except Exception as e:
            print(e)
            config.clear()
            return "Card not found in Inventory."

    if text == "%power":
        config.read(InventoryFilePath)
        cards = []
        for key, value in config.items(username):
            if int(value) > 1:
                for x in range(0, int(value)):
                    cards.append(await formatting.get_card_name(int(key)))
            else:
                cards.append(await formatting.get_card_name(int(key)))
        total_power = 0
        for card in cards:
            total_power += await formatting.get_card_power(card)
        config.clear()
        return "You have "+str(total_power)+" SmashBucks Power."

    if text == "%rarity":
        return "COMMON: 69.4%\nUNCOMMON: 20%\nRARE: 7%\nEPIC: 2%\nULTIMATE: 0.9%\nARTIFACT: 0.6%\nMYTHIC: 0.1%"

    if text == "%daily":
        output = await daily.daily(username)
        return output

    if text == "%puzzle":
        return "Checking the reason polling gives you cause for concern. 33.8% of the vote...\nYou'll lose in a landslide. Your map lies face up on the desk. Redraw...?\nPerhaps but you could only be so bold...\nYou'd need to make the districts the same size as one another, and they'd need to all be contiguous, surely no enclaves, diagonals or ties...\nThere's only 4 districts now... you could probably get away with changing that...\nCould purple actually become victorious? Currently, you wouldn't even win a single district.\n\nA faint whisper from the heavens:\n\n*DM me (not SmashBucks 2) a winning map*\n*And you'll need the map on your desk* \n*%map*\n\n(Puzzle uploaded 12/3/2024 @ 11:31 pm)"

    if text == "%leaderboard":
        config.read(InventoryFilePath)
        powers, players, final_power = [], [], [0]*5
        for player in config.sections():
            cards = []
            for key, value in config.items(player):
                if int(value) > 1:
                    for x in range(0, int(value)):
                        cards.append(await formatting.get_card_name(int(key)))
                else:
                    cards.append(await formatting.get_card_name(int(key)))
            total_power = 0
            for card in cards:
                total_power += await formatting.get_card_power(card)
            powers.append(total_power)
            players.append(player)
        powers = list(zip(powers, players))
        powers.sort()
        powers = powers[-5:]
        powers.reverse()
        for i in powers:
            players[powers.index(i)] = i[1]
            final_power[powers.index(i)] = i[0]
        placement = ["1. ", "2. ", "3. ", "4. ", "5. "]
        players = players[:5]
        for i in range(len(placement)):
            placement[i] = placement[i] + str(players[i]) + ": " + str(final_power[i])
        output = '\n'.join(placement)
        return output

    if text == "%opt in":
        config.read(PotatoFilePath)
        if await balance.userBalance(username) <= 0:
            return "You may not opt-in without any SmashBucks."
        if config.has_section(username):
            return "You are already opted in."
        return await potato.potato_opt_in(username)

    if text == "%opt out":
        config.read(PotatoFilePath)
        if config.getint('Setup', 'active') == 1:
            return f"You may not opt-out while someone is holding a live potato."
        if not config.has_section(username):
            return f"You are already opted out."
        return await potato.potato_opt_out(username)

    if text == "%create potato":

        enlarger = False
        holo_enlarger = False

        config.read(InventoryFilePath)

        for key in config.items(username):
            if key[0] == "122":
                enlarger = True
            if key[0] == "1122":
                holo_enlarger = True
                enlarger = False
                break

        if enlarger:
            damage = 1000
        elif holo_enlarger:
            damage = 1500
        else:
            damage = 500

        config.clear()

        config.read(PotatoFilePath)

        now = time.gmtime()
        current_time = time.mktime(now)

        if current_time < config.getfloat('Setup', 'lockout'):
            time_remaining = config.getfloat('Setup', 'lockout') - current_time
            hours = math.floor(time_remaining / 3600)
            time_remaining = time_remaining % 3600
            minutes = math.floor(time_remaining / 60)
            seconds = int(time_remaining % 60)
            z_mod_h = ""
            z_mod_m = ""
            z_mod_s = ""
            if hours < 10:
                z_mod_h = "0"
            if minutes < 10:
                z_mod_m = "0"
            if seconds < 10:
                z_mod_s = "0"
            return f"Cannot spawn a potato during the lockout period. ({z_mod_h}{hours}:{z_mod_m}{minutes}:{z_mod_s}{seconds} remaining)"

        if config.get('Setup', 'active') == 1:
            return "Cannot spawn potato while one is already active."

        lit_potato = potato.Potato(username, smashbucks, damage)
        return f"{username} is now holding a live potato."

    if re.search("%pass", text):
        target = text.replace("%pass ", "")
        target = await formatting.formatId(target)

        config.read(PotatoFilePath)

        if config.getint('Users', username) == 0:
            return "You cannot pass a potato when you aren't holding one."

        if config.getint('Users', target) == 1:
            return "Target is already holding a potato."

        if config.getint(username, "8") == 1:
            return "You are currently blackmailed!"

        for key, value in config.items('Users'):
            print(f"{key}: {value}")
            if key == target and int(value) == 0:
                try:
                    if config.getint(target, "7") == 1:
                        Mail(target, smashbucks)
                    return await lit_potato.pass_potato(target, username)

                except Exception as e:
                    print(f"Error: {e}")
        return "Target not among valid targets"

    if text == "%summon":
        return await game_actions.summon(username)

    if text == "%blink":
        return await game_actions.blink(username, smashbucks)

    if text == "%split":
        return await game_actions.split(username)

    if text == "%discover":
        return await game_actions.discover(username, lit_potato)

    if text == "%blackmail":
        return await game_actions.blackmail(username, smashbucks, lit_potato)

    if text == "%targets":
        config.read(PotatoFilePath)
        targets = []
        for section in config.sections():
            if not (section == "Users" or section == "Setup"):
                targets.append(section)
        if not targets:
            return "No one is currently opted in."
        return "Targets:\n"+"\n".join(targets)

    if text == "%uses":
        config.read(InitFilePath)
        uses = config.getint("init", "num_uses")
        uses = "{:,}".format(uses)
        return f"I've answered {uses} commands."
