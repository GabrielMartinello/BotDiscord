import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

cred = credentials.Certificate(r"./firebase_config.json")
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pythonbot-d31db-default-rtdb.firebaseio.com'
})

CHANNEL_ID = 1217901812359757947
users_ref = db.reference('/')
joinha = '\N{THUMBS UP SIGN}'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    verificar_vencedor.start()

@bot.command()
async def listar_comandos(ctx):
    response = 'Aqui estão alguns comandos que você pode solicitar para mim: \n!cumprimentos - Faz eu me apresentar'
    await ctx.send(response)

@bot.command()
async def regras(ctx):
    await ctx.send(mensagemRegras())

@bot.event
async def on_member_join(member):
    new_member_name = member.name
    print(f'Bem vindo ... {new_member_name}')
    default_channel = member.guild.system_channel

    users_snapshot = users_ref.get("Users")[0]
    if member.name in users_snapshot['Users']:
        response = f'Ueeehh {new_member_name} quis voltar pra tentar meter o shape de novo? Bora bater essas asas frangao'
        await default_channel.send(response)
    else:
        response = f'Olá {new_member_name} seja bem vindo, seu frango! '
        response += 'Vê se se esforça pra meter o shape, seu otário!\n'
        response += 'Regras:\n'
        response += mensagemRegras()
        await default_channel.send(response)

@bot.event
async def on_message(message):
    channelIDsToListen = [CHANNEL_ID]

    if message.channel.id in channelIDsToListen:
        if "#euFui" in message.content and message.attachments:
            for attachment in message.attachments:
                if any(ext in attachment.url.upper() for ext in ('PNG', 'JPG', 'JPEG', 'GIF')):
                    dataAtual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    users_ref.child("Users").child(str(message.author)).push({"Checkin": dataAtual})
                    await message.add_reaction(joinha)
                    await message.channel.send(f'Parabéns {message.author.name}! Sua presença acaba de ser confirmada!')

        await bot.process_commands(message)

@tasks.loop(hours=24)
async def verificar_vencedor():
    if datetime.now().day == 5:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            response = 'Salve, hoje é o dia de mostrar o vencedor CARAAALEEEOOO\n'
            ref = db.reference('Users')
            users_data = ref.get()

            if users_data:
                user_record_counts = {user_id: len(user_info) for user_id, user_info in users_data.items()}

                if user_record_counts:
                    vencedor_id = max(user_record_counts, key=user_record_counts.get)
                    vencedor_registros = user_record_counts[vencedor_id]
                    response += f'O vencedor é o usuário {vencedor_id} com {vencedor_registros} registros!\n'
                else:
                    response += 'Nenhum registro encontrado.\n'
            else:
                response += 'Nenhum usuário encontrado no banco de dados.\n'

            await channel.send(response)
        else:
            print(f'Canal com ID {CHANNEL_ID} não encontrado.')

def mensagemRegras():
    response =  '1. - Só vai contar como presença se a foto for postada no grupo com a tag #euFui!\n'
    response += '2. - Sua palavra pode valer alguma coisa, mas nesse grupo não! Somente fotos comprovam a presença\n'
    response += '3. - O ganhador receberá 10 reais de cada membro do grupo.'
    return response

load_dotenv()
bot.run(os.getenv('TOKEN'))
