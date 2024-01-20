#IMPORTAR BIBLIOTECAS E RECURSOS
import discord
from discord.ext import commands

import random
import time
import pytz

from datetime import datetime
from variaveis import ajuda_descricao, exposeds, fanfics, piadas
from keep_alive import keep_alive
keep_alive()

import os

#HABILITAR PERMISSÕES
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!rz ', intents=intents)
TOKEN = os.environ['TOKEN']

#COMANDOS
@bot.command() #!rz ajuda - O bot irá informar ao usuário os comandos que ele atende.
async def ajuda(ctx):
    comandos = discord.Embed(
        title = "*Heya!!* Meus Spawnpoint's:",
        description = ajuda_descricao,
        colour = 11598249
    )    
    await ctx.reply(embed=comandos)

@bot.command() #!rz dado - O bot irá rodar um dado e dirá o resultado.
async def dado(ctx, ld:int):
    lado = random.randint(1,ld)
    await ctx.reply(f'Caiu no {lado}!')

@bot.command() #!rz dia - O bot irá lhe informar que dia é hoje.
async def dia(ctx):
    pessoa = ctx.author
    
    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')
    data_hora_brasil = datetime.now(fuso_horario_brasil)
    dia = data_hora_brasil.strftime('%d/%m/%Y')
    
    await ctx.reply(f'Hoje é {dia} {pessoa.display_name}.')

@bot.command() #!rz diga (mensagem) - O bot vai repetir o que o user pediu e apagar a msg original.
async def diga(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)

@bot.command() #!rz exposed - O bot vai lhe informar o motivo de seu exposed.
async def exposed(ctx, pessoa:discord.Member):
    exposed = random.choice(exposeds).replace('user', pessoa.display_name)
    await ctx.reply(exposed)

@bot.command() #!rz fanfic - O bot irá contar um fanfic aleatória do servidor.
async def fanfic(ctx):
    fanfic = random.choice(fanfics)
    await ctx.reply(fanfic)

@bot.command() #!rz hora - O bot irá informar a hora atual.
async def hora(ctx:commands.Context):
    pessoa = ctx.author

    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')
    data_hora_brasil = datetime.now(fuso_horario_brasil)
    hora = data_hora_brasil.strftime('%H:%M:%S')
    
    await ctx.reply(f'Agora são {hora} {pessoa.display_name}.')

@bot.command() #!rz limpar (qt) - O bot irá limpar determinado número de mensagens do chat.
async def limpar(ctx, quantidade: int):
    # Verificar se o autor da mensagem tem permissão para limpar mensagens
    if ctx.message.author.guild_permissions.manage_messages:
        # Limpar mensagens no canal atual
        await ctx.channel.purge(limit=quantidade + 1)
        # Enviar uma mensagem indicando que as mensagens foram limpas
        await ctx.send(f'{quantidade} mensagens foram removidas.')
    else:
        # Se o autor não tiver permissões adequadas, enviar uma mensagem de aviso
        await ctx.send("Você não tem permissão para limpar mensagens.")

@bot.command() #!rz mandar (id_canal) (fala) - O bot irá mandar o que você disse no canal escolhido.
async def mandar(ctx, id_canal:int, *, fala):
    canal = bot.get_channel(id_canal)

    if canal is None:
        await ctx.send('Canal não encontrado!')
        return
    await canal.send(fala)

@bot.command() #!rz piada - O bot irá contar uma piada aleatória sobre Re:Zero.
async def piada(ctx):
    piada = random.choice(piadas)
    await ctx.reply(piada)

@bot.command() #!rz saudação - O bot irá saudar o usuário.
async def saudar(ctx):
    user = ctx.author
    await ctx.reply(f'> Heya {user.display_name}! Aqui é o bot. Retornando pela morte estou aqui para encarar qualquer desafio. A vida é cheia de reviravoltas, mas não se preocupe, estou sempre pronto para recomeçar!')

@bot.command() #!rz spam - O bot irá spamar quantas mensagens você quiser no chat.
async def spam(ctx, qt:int, *, frase):
    i = 0
    await ctx.message.delete()
    for i in range(qt):
        await ctx.send(frase)

#EVENTOS
@bot.event #Quando alguem escrever uma mensagem que contenha a palavra rem o usuário o responde.
async def on_message(pal:discord.Message):
    await bot.process_commands(pal)
    if pal.author == bot.user:
        return
    if 'rem' in pal.content.lower():
        await pal.reply('REM??????')
    elif 'loritta' in pal.content.lower():
        await pal.reply('Ela quer ser a rainha do humor, mas acho que seu código fonte está mais para uma comédia romântica do que para algum algoritmo eficiente :rofl:.')    

@bot.event #Quando o bot estiver online irá aparecer no console.
async def on_ready():
    print(f'{bot.user} está online!')
    canal = bot.get_channel(757649361248190546)
    await canal.send('Spawnpoint!')

#VALIDAR TOKEN
bot.run(TOKEN)
