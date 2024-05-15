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
    data_atual = datetime.now().date()
    mes_passado = data_atual.month - 1
                                
    if mes_passado == 0:
        mes_passado = 12
        ano_passado = data_atual.year - 1
    else:
        ano_passado = data_atual.year
        
    data_mes_passado = datetime(ano_passado, mes_passado, 1).date()      
      
    if data_atual.day == 15:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            response = 'Salve, hoje é o dia de mostrar o vencedor CARAAALEEEOOO\n'
            ref = db.reference('Users')
            users_data = ref.get()

            if users_data:
                user_record_counts = {}
                for user_id, user_info in users_data.items():
                    if isinstance(user_info, dict):
                        for registro_key, registro_data in user_info.items():
                            if isinstance(registro_data, dict) and 'Checkin' in registro_data:
                                checkin_date = datetime.strptime(registro_data['Checkin'], '%Y-%m-%d %H:%M:%S').date()
                                print(checkin_date, checkin_date.month, data_mes_passado, data_mes_passado.month)
                                if checkin_date.month == data_mes_passado.month and checkin_date.year == data_mes_passado.year:
                                    user_record_counts[user_id] = user_record_counts.get(user_id, 0) + 1

                vencedor = ''
                if user_record_counts:
                    top_users = sorted(user_record_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                    
                    # Montar a mensagem com o top 3 vencedores
                    for i, (user_id, record_count) in enumerate(top_users, start=1):
                        if i == 1:
                            response += f'{i}. - Usuário {user_id} com {record_count} registros (VENCEDOOOOOOR)\n'
                            vencedor = user_id
                        else:
                            response += f'{i}. - Usuário {user_id} com {record_count} registros\n'
                            
                    if vencedor: 
                        response += mensagemParabens(vencedor)                          
                else:
                    response += 'Nenhum registro encontrado no período anterior.\n'
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

def mensagemParabens(usuario):
    response =  f'Parabéns {usuario} seu frangote que fica enchendo a academia no verão, pelo menos você emagreceu uns kilos e chegou mais perto de alcançar o shape\n'
    response += 'Vê se continua assim, não para não meu querido!!!! Chris Bambister saindo, FIVE TIMES MR OLYMPIAANN!!\n'
    response += '---------------------------------------------------------------------------------------'
    return response

load_dotenv()
bot.run(os.getenv('TOKEN'))
