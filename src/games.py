import random
import discord
import asyncio
import os

possible_commands = ["roll", "rollnumber", "trivia", "score"]

async def play(client, command, args, message):
    """Takes input from on_message() and calls a function
    play() always returns a string."""

    if command == "score":
        await score(args[2:-1], message.channel, client)

    elif command == "roll":
        await client.send_message(message.channel, roll(args, message.server.members))

    elif command == "rollnumber":
        await client.send_message(message.channel, rollnumber(args))

    elif command == "trivia":
        args = args.split()
        try:
            game_length = int(args[0])
        except ValueError:
            game_length = 3
        try:
            difficulty = args[1]
        except IndexError:
            difficulty = random.choice(["lite", "easy", "medium", "hard"])
        await trivia(game_length, difficulty, message.channel, client)


##  SCOREBOARD FUNCTIONS  ##

def award_points(user, points):
    """Add a user's points to the scoreboard.
    NOTE: Assumes that data/scores.csv already exists"""
    with open("data/scores.csv", "r") as f:
        temp = open("data/temp.csv", "w")
        user_is_found = False

        for line in f:
            if line.split(',')[0] == user:  # if the current line matches the user
                old_points = int(line.split(',')[1])
                temp.write(user + "," + str(old_points + points) + "\n")
                user_is_found = True
            else:
                temp.write(line)  # if the current line is a different user

        if not user_is_found:
            temp.write("%s,%s\n" % (user, points))  # if the user isn't already in the scoreboard
        temp.close()

    os.remove("data/scores.csv")
    os.rename("data/temp.csv", "data/scores.csv")


def get_score(user):
    """Input a user, return their score as an int"""
    with open("data/scores.csv", "r") as f:
        for line in f:
            if line.split(',')[0] == user:
                return int(line.split(',')[1][:-1])
    return 0


async def score(id, channel, client):
    """Get a user's score! This function requires an argument
    e.g. `><>score @rishy 🐠y`"""
    user = await client.get_user_info(id)
    await client.send_message(channel, "<@" + user.id + "> has " + str(get_score(id)) + " points.")


##  OTHER FUNCTIONS  ##

def random_question(filename):
    q = ""
    a = "correct"
    while ("correct" in a.lower()) or ("following" in q.lower()):  # we do NOT want: answers flagged as incorrect, or "which of the following"-questions
        line = random_tsv_line(filename)
        column = random.randrange(0, len(line), 2)
        q = line[column]
        a = line[column + 1]
    return q, a


def random_tsv_line(filename):
    line = random.choice(list(open(filename, 'r'))).split('\t')
    if line[-1][-1] == "\n":
        line[-1] = line[-1][:-1]  # remove the '\n'
    return line


def make_hint(answer):
    """Randomly replaces most of the characters in a string with underscores"""
    outstr = ""
    for char in answer:
        if char.isalnum():
            if random.randint(0, 2) == 0:
                outstr += char + " "
            else:
                outstr += "_ "
        elif char == " ":
            outstr += "  "
        else:
            outstr += char
    # $char above and $char below this line are separate vars
    if sum(char.isalnum() for char in outstr) < len(answer)*0.2:
        return make_hint(answer)
    return outstr


def half_similar(a, b):
    """Finds if most of $a is in $b"""
    test = list(a.lower())
    check = list(b.lower())
    similarity = 0
    for character in test:
        if character in check:
            check.remove(character)
            similarity += 1
    if (similarity * 1.2) + 1 >= len(b):  # 1.2 means that 83% of the chars in $a must be in $b for success
        return True
    return False


##  GAME FUNCTIONS  ##

async def trivia(game_length, difficulty, channel, client):
    """Play a good ol' fashioned game of trivia!
    `><>trivia [number of questions] [difficulty]`
    potential difficulties: *lite, easy, medium, hard*
        e.g. `><>trivia 3 medium`"""

    def are_similar(message):
        """Finds if a message's content is similar to an answer
        Because this function is called as a check on wait_for_message(), only $message is accepted.
        Because only $message is accepted, $answer must be inherited
        Because $answer must be inherited, this function must lie within trivia()"""
        return half_similar(message.content, answer) and half_similar(answer, message.content)

    used_questions = []
    scoreboard = []
    await client.send_message(channel, "Starting " + difficulty + " trivia with " + str(game_length) + " questions!")

    for i in range(game_length):
        question, answer = random_question("data/trivia/" + difficulty + ".tsv")
        while question in used_questions:
            question, answer = random_question("data/trivia/" + difficulty + ".tsv")
        used_questions += [question]

        await client.send_message(channel, ":question:Trivia: **" + question + "**")
        await asyncio.sleep(1)
        await client.send_message(channel, "\thint: *`" + make_hint(answer) + "`*")

        guess = await client.wait_for_message(timeout=10.0, check=are_similar)

        if guess is None:
            await client.send_message(channel, "Good try! The correct answer was: **" + answer + "**")
        else:
            await client.send_message(channel, "Correct! %s got it with: **%s**" % (guess.author.name, answer))
            scoreboard += [guess.author.id]

        await asyncio.sleep(1)

    winner = await client.get_user_info(max(set(scoreboard), key=scoreboard.count))
    award_points(winner.id, scoreboard.count(winner.id))
    await client.send_message(channel, "Trivia complete! The winner was @%s#%s, with %s points!" % (winner.name, winner.discriminator, scoreboard.count(winner.id)))


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
        "I dunno about that.",
        "me too thanks",
        "Same",
        "moi aussi",
        "yo tambien"
    )

    if "rish" in question:
        if random.randint(1, 3) == 1:
            return "Idk man i think rishy's pretty cool."  # eyy

    # simple
    if question.split()[0].lower() in "do-does-can-will-should-is-am-was-are-were":
        return random.choice(default_responses)

    # 'who'
    if (question.startswith("who")) and not ("or " in question):
        return random.choice(list(members)).name

    # choices with fluff
    if (question.startswith("which")) or ("or " in question and "who " in question):
        # delete the question stem, saves the rest of the question in $choices
        separator = len(question)
        for character in ",:":
            try:
                separator = min(question.index(character), separator)
            except ValueError: pass
        # test break
        if separator == len(question):
            return random.choice(unsure_responses)

        choices = question[separator + 1:]
        # turn choices from a string with fluff, into a list without fluff
        choices = ''.join(x for x in choices if (x.isalnum() or ord(x) == 32))
        if "or " in choices:  # delete the word 'or'
            choices = choices.replace("or ", " ")
        choices = choices.split()

        # test break
        if choices == []:
            return random.choice(unsure_responses)

        # pick a random one
        return random.choice(choices)

    # choices separated by 'or'
    if " or " in question:
        choices = ''.join(x for x in question if (x.isalnum() or ord(x) == 32))
        choices = choices.split(" or ")
        return random.choice(choices)

    # 'how'
    if question.startswith("how"):
        return random.randint(1, 10*random.randint(1, random.randint(1, random.randint(1, 40)))) # gets a random number, more likely to be smaller but larger numbers are still possible

    # test break
    return random.choice(unsure_responses)
