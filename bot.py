from interactions import Client, Intents, listen, slash_command, SlashContext


bot = Client(intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)
# intents are what events we want to receive from discord
# `DEFAULT` et MESSAGE_CONTENT pour voir les messages


# this decorator tells snek that it needs to listen for the corresponding event
# and run this coroutine
@listen()
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    if event.message.author != bot.user:
        print(f"message received: {event.message.content}")


@slash_command(name="ping", description="ping pong")
async def ping_pong_command(ctx: SlashContext):
    await ctx.send("pong")

file = open(".token", "r")
bot.start(file.readline())
file.close()
