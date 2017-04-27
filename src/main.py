import discord
import logging
from time import strftime
import games
import param


# This 5-line block is copy-pasted from the discord.py docs
# https://discordpy.readthedocs.io/en/latest/logging.html
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print(strftime("Halibot is online! (%H:%M:%S)"))
    print("")


@client.event
async def on_message(message):

    if (message.author == client.user) or not(message.channel.name in param.permitted_channels):  # don't let the bot talk to itself or in an unallowed channel
        return

    if message.content.startswith('><>'):
        command = message.content.split()[0][3:]  # find the command

        try:
            args = message.content[message.content.index(" ") + 1:]  # finds the args if they exist
        except ValueError:
            args = ""

        if command in games.possible_commands:  # perform the command if possible
            await games.play(client, command, args, message)

        elif command == "help":
            if args == "":  # for blank help args
                await client.send_message(message.channel, "**List of commands**\n • " + "\n • ".join(games.possible_commands))

            elif len(args.split()) == 1:  # for correct help args
                try: await client.send_message(message.channel, args + ": " + eval('games.' + args + '.__doc__'))

                except AttributeError:  # for incorrect help args
                    await client.send_message(message.channel, "I don't recognize that function")

            else:
                await client.send_message(message.channel, "Sorry, I couldn't understand that")

        elif command == "quit":
            if message.author.id == param.owner_id:
                await client.send_message(message.channel, "Goodbye!")
                await client.logout()
                exit()
            else:
                await client.send_message(message.channel, "Stranger danger!")

        elif command == "":
            await client.send_message(message.channel, "<><")

    elif message.content == '<><':
        await client.send_message(message.channel, "><>")




client.run(param.token)