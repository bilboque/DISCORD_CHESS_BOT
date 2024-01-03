from interactions import Client, Intents, listen


bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord
# `DEFAULT` is usually fine


# this decorator tells snek that it needs to listen for the corresponding event
# and run this coroutine
@listen()
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event):
    # This event is called when a message is sent in a channel the bot can see
    print(f"message received: {event.message.content}")

file = open(".token", "r")
bot.start(file.readline())
file.close()
