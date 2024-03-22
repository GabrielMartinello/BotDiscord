import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv

intents = discord.Intents.all()
messages = []

bot = commands.Bot(command_prefix='!', intents=intents)

#reacoes
joinha = '\N{THUMBS UP SIGN}'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Comandos do bot
@bot.command()
async def cumprimentos(ctx):
    response = 'Olá, sou Chris Bambister e sou 5 vezes Mr Olympia! Estou aqui para lhe avaliar e anotar os dias que você foi na academia!'
    await ctx.send(response)

@bot.command()
async def listar_comandos(ctx):
    response = 'Aqui estão alguns comandos que você pode solicitar para mim: \n!cumprimentos - Faz eu me apresentar'
    await ctx.send(response)

@bot.command()
async def regras(ctx):
    response = 'Eu só sou um bot simples, oq vc me pedir lhe darei, menos minha dignidade'
    await ctx.send(response)
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(message.channel.id)
    
    channelIDsToListen = [ 1217901812359757947 ] # canais que o bot vai escutar

    if message.channel.id in channelIDsToListen:
        # Verifica se a mensagem contém "#euFui"
        if "#euFui" in message.content:
            if message.attachments:
                for attachment in message.attachments:
                  
                    # Verifica se o anexo é uma imagem
                    print(attachment.url)
                    if any(ext in attachment.url.upper() for ext in ('PNG', 'JPG', 'JPEG', 'GIF')):
                        await message.add_reaction(joinha)
                        await message.channel.send(f'Parabéns {message.author.name}! Sua presença acaba de ser confirmada!')
                        print(f"Mensagem com #euFui e uma imagem curtida por {bot.user.name}")        

# Pega o token do .env
load_dotenv()
bot.run(os.getenv('TOKEN'))
