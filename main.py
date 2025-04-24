import discord
import configparser
import bot
import asyncio
import os

config = configparser.ConfigParser()
InitFilePath = f"{os.getcwd()}/files/init.ini"
config.read(InitFilePath)
smashbucks_id = config.getint("init", "smashbucks_id")
token = config.get("init", "token")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
smashbucks = client.get_partial_messageable(id=smashbucks_id)

if __name__ == "__main__":
    asyncio.run(bot.run_discord_bot(token, client, smashbucks_id, smashbucks))
