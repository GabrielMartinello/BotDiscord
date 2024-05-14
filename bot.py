import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

cred = credentials.Certificate(r"./firebase_config.json")
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pythonbot-d31db-default-rtdb.firebaseio.com'
})

users_ref = db.reference('/')

#print(type(users_ref.get("Users")))
#users_data = users_ref.get("Users")
#users_data = users_data[0]

# Verifica se "Users" está presente nos dados e se "gabyrobot" é uma das chaves
#if 'Users' in users_data and 'gabyrobot' in users_data['Users']:
    #response = f'Ueeehh quis voltar pra tentar meter o shape de novo? Bora bater essas asas frangao'
    #print(response)
        
messages = []

#reacoes
joinha = '\N{THUMBS UP SIGN}'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

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
    channelIDsToListen = [ 1217901812359757947 ] # canais que o bot vai escutar

    if message.channel.id in channelIDsToListen or message.content.startswith('!'):
        # Verifica se a mensagem contém "#euFui"
        if "#euFui" in message.content:
            if message.attachments:
                for attachment in message.attachments:
                    # Verifica se o anexo é uma imagem
                    if any(ext in attachment.url.upper() for ext in ('PNG', 'JPG', 'JPEG', 'GIF')):
                        dataAtual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        users_ref.child("Users").child(str(message.author)).push({"Checkin": dataAtual})
                        await message.add_reaction(joinha)
                        print(f"Mensagem com #euFui e uma imagem curtida por {bot.user.name}")
                        await message.channel.send(f'Parabéns {message.author.name}! Sua presença acaba de ser confirmada!')
           
        await bot.process_commands(message)
        
@bot.event
async def verifica_dia_resultado_vencedor(ctx):
    data_atual = datetime.now()
    if data_atual.day == 1:
        response = 'Salve, hoje é o dia de mostrar o vencedor caraleo\n'
        #Mostrar o vencedor
        
def mensagemRegras():
    response =  '1. - Só vai contar como presença se a foto for postada no grupo com a tag #euFui!\n'
    response += '2. - Sua palavra pode valer alguma coisa, mas nesse grupo não! Somente fotos comprovam a presença\n'
    response += '3. - O ganhador receberá 10 reais de cada membro do grupo.'
    return response            
                 
load_dotenv()
bot.run(os.getenv('TOKEN'))
