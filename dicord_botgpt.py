import openai
import random
import discord
from discord.ext.commands import Bot

#Api Key OpenAI
openai.api_key ='poner_apikey_openai'

#Token Bot de Discord
token_discord='poner_token_discord'

nombre_bot = 'BotGPT'

personalidad= [{"role": "system", "content":f"Eres un bot de discord llamado {nombre_bot}. Debes responder comenzando con {nombre_bot}: "},
        {"role": "system", "name": "example_assistant","content": f"{nombre_bot}: Hola a todos!"},
        #{"role": "system", "content":f"Caracteristicas del bot"},
        #{"role": "system", "content":f"Caracteristicas del bot"},
        #{"role": "system", "content":f"Caracteristicas del bot"},
     ]

intents = discord.Intents.all()
bot = Bot(command_prefix='!', intents=intents)

mensajes=[]
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="computando")) #Jugando a "computando" (opcional)
    print(f'Te haz logueado como {bot.user}')

@bot.event
async def on_message(message):
    canal = message.channel
    canal_name = message.channel.name
    messages = []

    aleatorio = random.randint(0, 100)
    print(canal)
    print(aleatorio)

    #Probabilidad de que el bot responda sin ser llamado aleatorio>=0 (100%), aleatorio>100 (0%)
    if canal_name == 'general' and aleatorio>=70:
        async with canal.typing():

            #Se almacenan los ultimos mensajes que seran enviados al bot
            #Limit define la cantidad de mensajes que lee el bot para gestionar la respuesta
            async for msg in canal.history(limit=25):
                if msg.author.name != nombre_bot and not msg.content.startswith('!'):
                    mensaje_user = f'{msg.author.display_name}: {msg.content}'
                    messages.append({"role": "user", "content": mensaje_user})

                if msg.author.name == nombre_bot and not msg.content.startswith('!'):
                    mensaje_assistant = (f'{msg.author.display_name}: {msg.content}')
                    messages.append({"role": "assistant", "content": mensaje_assistant})

            messages=list(reversed(messages))
            print(messages)

            #Se envia la personalidad y los últimos mensajes al servidor de OpenAI
            if message.author.name != nombre_bot and not message.content.startswith('!'):
                mensajes = personalidad + messages

                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=mensajes)
                #response = openai.ChatCompletion.create(model="gpt-4", messages=mensajes)
                print(response.choices[0].message.content)
                print("------")
                await message.channel.send(response.choices[0].message.content.lstrip(f"{nombre_bot}:"))


    if message.content.startswith('!'):
        # Procesamos el comando
        await bot.process_commands(message)
        return


@bot.command()
async def ia(ctx):
    canal=ctx.channel
    message=ctx.message
    print(message.content)
    print(message.author.name)
    messages = []

    async with canal.typing():

        # Se almacenan los ultimos mensajes que seran enviados al bot
        # Limit define la cantidad de mensajes que lee el bot para gestionar la respuesta
        async for msg in canal.history(limit=100):
            if msg.author.name != nombre_bot and not msg.content.startswith('!'):
                mensaje_user = f'{msg.author.display_name}: {msg.content}'
                messages.append({"role": "user", "content": mensaje_user})

            if msg.author.name == nombre_bot and not msg.content.startswith('!'):
                mensaje_assistant = (f'{msg.author.display_name}: {msg.content}')
                messages.append({"role": "assistant", "content": mensaje_assistant})

            if msg.author.name != nombre_bot and msg.content.startswith('!ia'):
                mensaje_user = f'{msg.author.display_name}: {msg.content}'
                messages.append({"role": "user", "content": mensaje_user})

        messages = list(reversed(messages))
        print(messages)

        if message.author.name != nombre_bot:

            mensajes = personalidad + messages
            #response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=mensajes)
            response = openai.ChatCompletion.create(model="gpt-4", messages=mensajes)
            print(response.choices[0].message.content)
            print("------")

            await message.channel.send(response.choices[0].message.content.lstrip(f"{nombre_bot}:"))

bot.run(token_discord)