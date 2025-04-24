import discord
import configparser
import responses
import balance
import os

config = configparser.ConfigParser()
ClientListFilePath = f"{os.getcwd()}/files/client_list.ini"
InventoryFilePath = f"{os.getcwd()}/files/inventory.ini"
InitFilePath = f"{os.getcwd()}/files/init.ini"


async def output_message(message, smashbucks):
    try:
        response = await responses.handleResponse(message, smashbucks)
        if isinstance(response, tuple):
            await message.author.send(response[0])
        else:
            await message.channel.send(response)

    except Exception as e:
        print(f"Error: {e} ({message.content})")

    else:
        use_incrementer = configparser.ConfigParser()
        use_incrementer.read(InitFilePath)

        uses = use_incrementer.get('init', 'num_uses')
        uses = int(uses) + 1
        use_incrementer.set('init', 'num_uses', str(uses))
        with open(InitFilePath, "w") as configfile:
            use_incrementer.write(configfile)
        use_incrementer.clear()


async def run_discord_bot(token, client, smashbucks_id, smashbucks):

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.channel.id != smashbucks_id and message.author.name != 'arjay_tg':
            return
        try:
            username = str(message.author)
            config.read(ClientListFilePath)
            users = []
            for key, value in config.items('client_list'):
                users.append(key)
            if username not in users:
                config['client_list'][username] = str(message.author.id)
                with open(ClientListFilePath, 'w') as configfile:
                    config.write(configfile)
                config.clear()
                await init_user(message.author.name)
            await output_message(message, smashbucks)
        except Exception as e:
            print(e)
    await client.start(token, reconnect=True)


async def init_user(username):
    print("Welcome to SmashBucks "+username)
    await balance.initUserBalance(username)
    config.read(InventoryFilePath)
    try:
        config.add_section(username)
        config[username]["31"] = "1"
        with open(InventoryFilePath, "w") as configfile:
            config.write(configfile)
        config.clear()
    except Exception as e:
        print(e)











