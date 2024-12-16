import re
import balance
import formatting
import flavor
import beg
import configparser
import daily

config = configparser.ConfigParser()
InventoryFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/inventory.ini"
PuzzleFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/puzzle.ini"


async def handleResponse(message):
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
        return "%beg\n%balance\n%gacha\n%sell\n%inventory\n%prices\n%power\n%rarity\n%puzzle"

    if text == "%random_card":
        if username == "arjay_tg" or username == "_camden":
            card_id = await formatting.card_shuffler()
            file_path = await formatting.display_card(card_id)
            await formatting.output_card(file_path, message.channel)
            return
        else:
            return "Access Denied."

    if text == "%gacha":
        current_balance = await balance.userBalance(message.author.name)
        if current_balance >= 20:
            output = await balance.botSubBalance(message.author.name, 20)
            card_id = await formatting.card_shuffler()
            file_path = await formatting.display_card(card_id)
            await formatting.output_card(file_path, message.channel)
            config.read(InventoryFilePath)
            cards = []
            for key, value in config.items(username):
                cards.append(key)
            print(cards)
            print(card_id)
            print(str(card_id) in cards)
            if str(card_id) in cards:
                print("found")
                config[username][str(card_id)] = str(config.getint(username, str(card_id)) + 1)
            else:
                config[username][str(card_id)] = "1"
            with open(InventoryFilePath, "w") as configfile:
                config.write(configfile)
                config.clear()
            return output
        else:
            return "Insufficient Funds"

    if text == "%inventory":
        config.read(InventoryFilePath)
        cards = []
        for key, value in config.items(username):
            name = await formatting.get_card_name(int(key))
            name.replace("_", "'")
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
        text = text.upper()
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
            return "It is unwise to sell such a priceless item.\n-Someone Wise, probably"

    if text == "%prices":
        return "COMMON: 7 Smashbucks\nUNCOMMON: 18 Smashbucks\nRARE: 40 Smashbucks\nEPIC: 100 Smashbucks\nULTIMATE: 250 Smashbucks\nMYTHIC: 1000 Smashbucks"

    if re.search("%view*", text):
        text.replace("'", "_")
        text = text.replace("%view ", "")
        text = text.upper()
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
        print(cards)
        for card in cards:
            total_power += await formatting.get_card_power(card)
        config.clear()
        return "You have "+str(total_power)+" SmashBucks Power."

    if text == "%rarity":
        return "COMMON: 70%\nUNCOMMON: 20%\nRARE: 7%\nEPIC: 2%\nULTIMATE: 0.9%\nMYTHIC: 0.1%"

    if text == "%daily":
        output = await daily.daily(username)
        return output

    if text == "%puzzle":
        return "There are no currently active puzzles."
    if text == "%taskmaster":
        config.read(PuzzleFilePath)
        if config.getboolean("Shard of Taskmaster", "completed"):
            return "Puzzle has already been completed."
        else:
            config["Shard of Taskmaster"]["completed"] = "1"
            with open(PuzzleFilePath, "w") as configfile:
                config.write(configfile)
            config.clear()
            file_path = await formatting.display_card(122)
            await formatting.output_card(file_path, message.channel)
            config.read(InventoryFilePath)
            config[username]["122"] = "1"
            with open(InventoryFilePath, "w") as configfile:
                config.write(configfile)
            return "The fair arbiter's words held true. Taskmaster's essence, his residual malice, now lies in your possesion."

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

    if text == "%tome_of_inquisition":
        config.read(PuzzleFilePath)
        if config.getboolean("Tome of Inquisition", "completed"):
            return "Puzzle has already been completed."
        else:
            config["Tome of Inquisition"]["completed"] = "1"
            with open(PuzzleFilePath, "w") as configfile:
                config.write(configfile)
            config.clear()
            file_path = await formatting.display_card(123)
            await formatting.output_card(file_path, message.channel)
            config.read(InventoryFilePath)
            config[username]["123"] = "1"
            with open(InventoryFilePath, "w") as cfile:
                config.write(cfile)
            return "The secrets of creation sparkle at your fingertips. Now if only you could read the ancient tongue."

    if re.search('%gen_truth_table "*', text):
        text = text[18:-1]
        if 'z' in text:
            rows = [ [0]*8 for i in range(8)]
            x = [0,0,0,0,1,1,1,1]
            y = [0,0,1,1,0,0,1,1]
            z = [0,1,0,1,0,1,0,1]
            for i in range(8):
                rows[i].append(x[i])
                rows[i].append(y[i])
                rows[i].append(z[i])
            print(rows)



















