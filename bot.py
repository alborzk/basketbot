import discord
import responses

async def send_messsage(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTA0MjM0MzEyMTgyMTkwNDk3Ng.GYepoX.CwjvriFRYEBnj5q9HszG9-FUajlNkb9q-yFa8I'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} sent a message in {channel}: {user_message}')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_messsage(message, user_message, is_private=True)
        else:
            await send_messsage(message, user_message, is_private=False)

    client.run(TOKEN)