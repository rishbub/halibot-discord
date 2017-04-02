import random


def play(command, args, author, channel, server):
    """Takes input from handler() and calls a function
    play() always returns a string."""  # This alt text should not be viewed under help()
    if command == "roll":
        if args == "":
            return ("?")
        return roll(args, server.members)
    if command == "rollnumber":
        return rollnumber(args)


def rollnumber(number):
    """Input a number and roll a die with that many sides
    (e.g. `><>rollnumber 6`)"""
    try:
        return str(random.choice(range(1, int(number)+1)))
    except:
        return "I don't like that number."


def roll(question, members):
    """Input a question and find out its answer.
    (e.g. `><>roll who is my crush?`)"""

    questiontype = question.split()[0].lower()

    if "rish" in question:
        if random.randint(1, 5) == 5:
            return "Idk man i think rishy's pretty cool."  # eyy

    # simple
    if questiontype in "do-does-can-will-should-is-am-was-are-were":
        return random.choice(default_responses)

    # 'who'
    if (questiontype[:3] == "who") and not ("or " in question):
        return random.choice(list(members)).name

    # choices with fluff
    if (questiontype == "which") or ("or " in question and "who " in question):
        # delete the question stem, saves the rest of the question in $choices
        separator = len(question)
        for character in ",:":
            try:
                separator = min(question.index(character), separator)
            except ValueError: pass
        # test break
        if separator == len(question):
            return "Sorry, I couldn't understand your question (couldn't separate)"

        choices = question[separator + 1:]
        # turn choices from a string with fluff, into a list without fluff
        choices = ''.join(x for x in choices if (x.isalnum() or ord(x) == 32))
        if "or " in choices:  # delete the word 'or'
            choices = choices.replace("or ", " ")
        choices = choices.split()

        # test break
        if choices == []:
            return "Sorry, I couldn't understand your question (no choices left)"

        # pick a random one
        return random.choice(choices)

    # choices separated by 'or'
    if " or " in question:
        choices = ''.join(x for x in question if (x.isalnum() or ord(x) == 32))
        choices = choices.split(" or ")
        return random.choice(choices)

    # 'how many' TODO
    if questiontype == "how":
        if question.split()[1] in "do-does-can-will-should-is-am-was-are-were"):
            pass
        else:
            return random.randint(1, 10*random.randint(1, random.randint(1, random.randint(1, 40)))) #gets a random number, more likely to be smaller but larger numbers are still possible

    # test break
    return random.choice(unsure_responses)


default_responses = (
            "Yes.",
            "Certainly!",
            "Mhm!",
            "Yep.",
            "You betcha!",
            "Nope.",
            "Definitely not.",
            "Eww, no!"
            "Why not?"
            "Maybe.",
            "Who knows?",
            "Seems fishy.",
            "That seems pretty fishy.",
            "That's up for debate.",
            "Probably.",
            "Probably not.",
            "ಠ_ಠ",  # look of disapproval
            "( ͡° ͜ʖ ͡°)",
            "¯\_(ツ)_/¯"
        )

unsure_responses = (
    "Now, how would I know?",
    "You tell me.",
    "Beats me.",
    "Hmm...",
    "I dunno about that."
    "me too thanks",
    "Same"
    "moi aussi",
    "yo tambien"
)