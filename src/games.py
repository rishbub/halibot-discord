import random
import discord

def roll(message):
    questiontype = message.content.split()[1].lower()
    if (questiontype == "who") and not ("or " in message.content):  # for 'who' questions without choices
        return random.choice(list(message.server.members)).name

    #this block is still in progress
    if (questiontype == "which") or (questiontype == "who" and "or " in message.content):  # for any questions with choices
        # delete the question stem, saves the rest of the question in $choices
        separator = len(message.content)
        for character in ",:?":
            try:
                separator = min(message.content.index(character), separator)
            except ValueError:
                pass
        if separator == len(message.content):
            return "Sorry, I couldn't understand your question"
        choices = message.content[separator + 1:]

        # turn choices into a list of options
        choices = ''.join(x for x in choices if x.isalnum())  # delete all non-alphanumeric characters
        if "or " in choices:  # delete the word 'or'
            choices.replace("or ", " ")
        choices.split()

        if choices == []:
            return "Sorry, I couldn't understand your question"
        # pick a random one
        return random.choice(choices)

    string = '''\n''' + message.content + '''\n''' +  '''\n''' + questiontype
    return string