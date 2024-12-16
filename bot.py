import discord
import configparser
import responses
import balance

config = configparser.ConfigParser()
ClientListFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/client_list.ini"
InventoryFilePath = "/home/pendleton/PycharmProjects/SmashBucks2/.venv/files/inventory.ini"


async def output_message(message, smashbucks):
    try:
        response = await responses.handleResponse(message)
        await message.channel.send(response)

    except Exception as e:
        print(e)


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
    except Exception as e:
        print(e)











