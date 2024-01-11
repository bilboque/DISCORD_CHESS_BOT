from interactions import Client, Intents, listen
from interactions import StringSelectMenu, StringSelectOption
from interactions import slash_command, slash_option, OptionType
from interactions import SlashContext, SlashCommandChoice
import chess
import berserk
import requests
from json import loads


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


# exemple d'une / command avec des optione
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
    if level < 1 or level > 8:
        await ctx.send("Le niveau du bot doit être entre 1 et 8")
        return

    f = open(".tokenleo", "r")
    session = berserk.TokenSession(f.readline())
    f.close()

    client = berserk.Client(session=session)
    challenge_info = client.challenges.create_ai(level=level)
    stream = client.board.stream_game_state(challenge_info['id'])
    event = next(stream)
    if 'id' in event['white']:
        await ctx.send(f"You play as **white** --> game id=**{challenge_info['id']}**")
    else:
        await ctx.send(f"You play as **black** (1: {event['state']['moves']}) --> game id=**{challenge_info['id']}**")


@slash_command(name="move", description="Usage /move gameID")
@slash_option(
        name="gameid",
        description="id donné par le bot précédemment",
        required=True,
        opt_type=OptionType.STRING,
)
async def make_a_moove_in_lichess_game(ctx: SlashContext, gameid):
    f = open(".tokenleo", "r")
    session = berserk.TokenSession(f.readline())
    f.close()

    client = berserk.Client(session=session)
    stream = client.games.stream_game_moves(gameid)
    event = next(stream)

    if event['status']['name'] != "started":
        try:
            await ctx.send(f"this game is over:\n- status: {event['status']['name']}\n- winner: {event['winner']}")
        except:
            await ctx.send("something went wrong")
        return

    board = chess.Board()
    board.set_epd(event['fen'])

    mv_list = []
    for moove in board.legal_moves:
        # str pour deref le generator je ne sais pas pourquoi ca marche
        mv_list.append(str(moove))

    components = StringSelectMenu(
        placeholder="legal moves",
        min_values=1,
        max_values=1,
    )
    components.options = [StringSelectOption(label=a, value=a) for a in mv_list[:24]]
    await ctx.send(f"{board.unicode()}", components=components)
    response = await bot.wait_for_component(components=components)
    client.board.make_move(gameid, response.ctx.values[0])
    await ctx.send(f"move played {response.ctx.values[0]}")


@slash_command(name="resign", description="Usage /resign gameID")
@slash_option(
        name="gameid",
        description="id donné par le bot précédemment",
        required=True,
        opt_type=OptionType.STRING,
)
async def resign_lichess_game(ctx: SlashContext, gameid):
    f = open(".tokenleo", "r")
    session = berserk.TokenSession(f.readline())
    f.close()

    client = berserk.Client(session=session)
    try:
        client.board.resign_game(game_id=gameid)
    except:
        await ctx.send(f"invalid game id (id={gameid})")
    else:
        await ctx.send(f"you resigned in your game (id={gameid})")


@slash_command(name="tournois", description="Usage /tournois")
async def trounois_infos(ctx: SlashContext):
    r = requests.get("http://127.0.0.1:5000/api/tournois_infos")
    data = loads(r.text)
    msg = "The tournaments played ad UNIGE chessclub:"
    for elem in data['data']:
        msg += f"\n- **{elem['nom']}**, {elem['date']} (id={elem['id']})"
    await ctx.send(msg)


@slash_command(name="resultats", description="Usage /resultat tournoiID")
@slash_option(
        name="id",
        description="id du tournois",
        required=True,
        opt_type=OptionType.INTEGER,
)
async def tournois_result(ctx: SlashContext, id):
    r = requests.get(f"http://127.0.0.1:5000/api/tournoi/{id}")
    data = loads(r.text)
    msg = f"Resultat du tounoi **{((data['data'])[0])['tournoi']}**"
    for elem in data['data']:
        msg += f"\n- {elem['resultat']} : **{elem['nom']}** avec {elem['points']} points"
    await ctx.send(msg)


# start the bot
file = open(".token", "r")
bot.start(file.readline())
file.close()
