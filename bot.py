from interactions import Client, Intents, listen
from interactions import slash_command, slash_option, OptionType
from interactions import SlashContext, SlashCommandChoice
from interactions import Modal, ModalContext, ShortText
import berserk


bot = Client(intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)
# intents are what events we want to receive from discord
# `DEFAULT` et MESSAGE_CONTENT pour voir les messages


# Log sur sdtout quand le bot est connecté au server
@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


# Log sur stdout les messages des users
@listen()
async def on_message_create(event):
    if event.message.author != bot.user:
        print(f"message received: {event.message.content}")


# Basic / command avec des optione
# /ping ping -> pong dans le channel en question,
# /ping pong -> ping dans le channel en question
@slash_command(name="ping", description="Usage /ping [ping, pong]")
@slash_option(
        name="ping_options",
        description="ping ou pong",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="ping", value="ping"),
            SlashCommandChoice(name="pong", value="pong"),
        ]
)
async def ping_pong_command(ctx: SlashContext, ping_options):
    if ping_options == "ping":
        await ctx.send("pong")
    elif ping_options == "pong":
        await ctx.send("ping")


@slash_command(name="play", description="Usage /play level")
@slash_option(
        name="level",
        description="choose stockfish level",
        required=True,
        opt_type=OptionType.INTEGER,
)
async def create_lichess_game(ctx: SlashContext, level):
    f = open(".tokenleo", "r")
    session = berserk.TokenSession(f.readline())
    f.close()

    client = berserk.Client(session=session)
    challenge_info = client.challenges.create_ai(level=level)
    stream = client.board.stream_game_state(challenge_info['id'])
    event = next(stream)
    if 'id' in event['white']:
        await ctx.send(f"You play as **white** --> game id :**{challenge_info['id']}**")
    else:
        await ctx.send(f"You play as **black** (1: {event['state']['moves']}) --> game id :**{challenge_info['id']}**)")


file = open(".token", "r")
bot.start(file.readline())
file.close()
