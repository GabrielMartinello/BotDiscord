import discord
import os
from discord.ext import commands 
from dotenv import load_dotenv
import botDao
import pandas as pd

# Create a Discord client instance and set the command prefix
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
# Set the confirmation message when the bot is ready

messages = []

pessoa_sql = """
    CREATE TABLE pessoa (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(60) NOT NULL
    )
"""

presenca_sql = """
    CREATE TABLE presenca (
        id SERIAL PRIMARY KEY,
        dataPresenca DATE NOT NULL,
        pessoa_id SERIAL REFERENCES pessoa(id)
    )
"""

#reacoes
joinha = '\N{THUMBS UP SIGN}'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Comandos do bot
@bot.command()
async def cumprimentos(ctx):
    print('Veio aqui')
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
    
@bot.command()
async def criar_tabelas_pg(ctx):    
    print('Criando tabelas...')
    botDao.create_table_by_command(pessoa_sql)
    botDao.create_table_by_command(presenca_sql)
    
@bot.event
async def on_member_join(member):
    # Obtém o nome do novo membro
    new_member_name = member.name
    print(f'Bem vindo ... {new_member_name}')
    df = pd.DataFrame({"nome": [new_member_name]})
    
    # Consulta SQL para verificar se o nome já existe na tabela pessoa
    existing_data = botDao.getData_from_database(f"SELECT * FROM pessoa WHERE nome = '{new_member_name}'")
    
    if not existing_data.empty:
        print(f"O nome '{new_member_name}' já existe na tabela pessoa. Não adicionando novamente.")
        return
    
    sql = "INSERT INTO pessoa (nome) VALUES %s"
    botDao.insert_dataTable_by_comand(sql, df)
    print(f"Novo membro '{new_member_name}' adicionado à tabela pessoa.")
    
    default_channel = member.guild.system_channel
    
    if default_channel is not None:
        # Envia uma mensagem de boas-vindas para o novo membro
        response = f'Olá {new_member_name} seja bem vindo, seu frango! Estou te adicionando em nossa base de dados, vê se se esforça pra meter o shape, seu otário!'
        await default_channel.send(response)
    else:
        print("Canal padrão para novos membros não encontrado.")
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(message.channel.id)
    
    channelIDsToListen = [ 1217901812359757947 ] # canais que o bot vai escutar

    if message.channel.id in channelIDsToListen or message.content.startswith('!'):
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

        await bot.process_commands(message)                      

# Pega o token do .env
load_dotenv()
print(os.getenv('TOKEN'))
bot.run(os.getenv('TOKEN'))
