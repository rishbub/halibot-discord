import discord
import logging
import games
import os
import asyncio

# This block is copy-pasted from the docs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Get the parameters
print("Getting the parameters...")
param = open("param.txt", "r")
token = param.readline().replace("\n", "")  # the  first line of param.txt is the token
command_phrase = param.readline().replace("\n", "")  # the second line of param.txt is the command phrase
param.close()

client = discord.Client()



@client.event
async def on_ready():
    print("Starting Halibot...")
    print("")


@client.event
async def on_message(message):
    if message.content.startswith(command_phrase):
        command = message.content.split()[0][3:]
        if command == 'roll':
            print(games.roll(message))
            #await client.send_message(message.channel, games.roll(message))


client.run(token)
