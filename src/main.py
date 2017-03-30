import discord
import logging
import os
import asyncio

#This block is copy-pasted from the docs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Get the parameters
print("Getting the parameters...")
param = open("param.txt", "r")
token = param.readline().replace("\n","")
command_phrase = param.readline().replace("\n","")
param.close()

client = discord.Client()

@client.event
async def on_ready():
    print ("Starting Halibot...")
    print ("")

@client.event
async def on_message(message):
    if message.content.startswith('><>'):
        await client.send_message(message.channel, 'Say hello')
        msg = await client.wait_for_message(author=message.author, content='hello')
        await client.send_message(message.channel, 'Hello.')

client.run(token)