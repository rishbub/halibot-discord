import discord
import logging
import games
import asyncio

# This 5-line block is copy-pasted from the discord.py docs
# https://discordpy.readthedocs.io/en/latest/logging.html
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
    def channel_out(text):
        return "client.send_message(message.channel,'"+text+"')"

    if message.content.startswith(command_phrase):
        command = message.content.split()[0][len(command_phrase):]  # find the command

        try: args = message.content[message.content.index(" ") + 1:]  # finds the args if they exist
        except: args = ""

        if command == "help":
            if args == "":  # for blank args
                await client.send_message(message.channel, "**List of commands**\n" + "\n".join(command_list))

            elif args == "[command]":  # for stupid args
                await client.send_message(message.channel, "Don't you know what brackets stand for?")

            elif len(args.split()) == 1:  # for correct args
                try: await client.send_message(message.channel, args + ": "+ eval('games.' + args + '.__doc__'))

                except AttributeError:
                    await client.send_message(message.channel, "I don't recognize that function")

            else:
                await client.send_message(message.channel, "Sorry, I couldn't understand that")

        elif command in command_list:
            await client.send_message(message.channel, games.play(command, args, message.author, message.channel, message.server))
        else:
            await client.send_message(message.channel, "Try `><>help [command]`")



command_list = ["roll", "rollnumber"]
client.run(token)
