#IMPORTAR BIBLIOTECAS E RECURSOS
import discord, giphy_client, pytz, random, requests

from discord.ext import commands
from giphy_client.rest import ApiException
from faker import Faker
from bs4 import BeautifulSoup
from datetime import datetime
from variaveis import ajuda_descricao, curiosidades, emojis, exposeds, fanfics, informacoes, piadas, risadas, xingamentos
from keep_alive import keep_alive
keep_alive()

import os

#HABILITAR PERMISSÕES
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!rz ', intents=intents)
TOKEN = os.environ['TOKEN']
api_key = os.environ['API_GIPHY']
api_instance = giphy_client.DefaultApi()

#COMANDOS
@bot.command() #!rz ajuda - O bot irá informar ao usuário os comandos que ele atende.
async def ajuda(ctx):
    comandos = discord.Embed(
        title = "*Heya!!* Meus Spawnpoint's:",
        description = ajuda_descricao,
        color = discord.Color.green())    
    await ctx.reply(embed=comandos)

@bot.command() #!rz banir (@usuário) - O bot irá banir o usuário mencionado.
async def banir(ctx:commands.Context, user:discord.Member):
    autor = ctx.author
    if ctx.message.author.guild_permissions.ban_members:
        await ctx.guild.ban(user)
        await ctx.reply(f'O/A {user.display_name} foi banido(a) desse mundo! Parece que suas ações romperam os laços do espaço-tempo, e agora estão proibidos de interagir em nosso universo.')
    else:
        await ctx.reply(f'{autor} pare de tentar banir as pessoas! Caso contrário o próximo será você..')

@bot.command() #!rz curiosidades - O bot irá dizer uma curiosidade.
async def curiosidade(ctx):
    curiosidade = random.choice(curiosidades)
    await ctx.reply(curiosidade)

@bot.command() #!rz dado - O bot irá rolar um dado e dirá o resultado.
async def dado(ctx, ld:int):
    lado = random.randint(1,ld)
    await ctx.reply(f'Caiu no {lado}!')

@bot.command() #!rz desbanir (id_user) - O bot irá desbanir o usuário.
async def desbanir(ctx, member_id:int):
    usuarios_banidos = []
    async for ban_entry in ctx.guild.bans():
        usuarios_banidos.append(ban_entry.user)

    # Agora você pode trabalhar com a lista de usuários banidos
    user_to_unban = discord.utils.get(usuarios_banidos, id=int(member_id))

    if user_to_unban:
        await ctx.guild.unban(user_to_unban)
        await ctx.send(f'O membro {user_to_unban.mention} foi desbanido! Em nome de Emilia, a justiça foi feita.')
    else:
        await ctx.send('Membro não encontrado na lista de banidos.')

@bot.command() #!rz dia - O bot irá lhe informar que dia é hoje.
async def dia(ctx):
    pessoa = ctx.author
    
    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')
    data_hora_brasil = datetime.now(fuso_horario_brasil)
    dia = data_hora_brasil.strftime('%d/%m/%Y')
    
    await ctx.reply(f'Hoje é {dia} {pessoa.mention}.')

@bot.command() #!rz diga (mensagem) - O bot vai repetir o que o user pediu e apagar a msg original.
async def diga(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)

@bot.command() #!rz exposed - O bot vai lhe informar o motivo de seu exposed.
async def exposed(ctx, pessoa:discord.Member):
    exposed = random.choice(exposeds).replace('user', pessoa.mention)
    await ctx.reply(exposed)

@bot.command() #!rz fanfic - O bot irá contar um fanfic aleatória do servidor.
async def fanfic(ctx):
    fanfic = random.choice(fanfics)
    await ctx.reply(fanfic)

@bot.command() #!rz gif (termo) - O bot enviará um gif relacionado ao termo mencionado.
async def gif(ctx, *, termo):
    embed = discord.Embed(title=f'Gif relacionado a "{termo}":', color=discord.Color.green())
    try:
        # Pesquisar gif no Giphy
        response = api_instance.gifs_search_get(api_key, termo, limit=1)
        
        # Obter a URL do gif
        gif_url = response.data[0].images.fixed_height.url

        # Enviar a URL do gif no canal do Discord
        embed.set_image(url=gif_url)
        await ctx.reply(embed=embed)

    except ApiException as e:
        print(f"Erro ao buscar gif: {e}")
        await ctx.send(f"Ocorreu um erro ao buscar o gif relacionado a '{termo}'.")

@bot.command() #!rz hora - O bot irá informar a hora atual.
async def hora(ctx:commands.Context):
    pessoa = ctx.author

    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')
    data_hora_brasil = datetime.now(fuso_horario_brasil)
    hora = data_hora_brasil.strftime('%H:%M:%S')
    
    await ctx.reply(f'Agora são {hora} {pessoa.mention}.')

@bot.command() #!rz info - O bot irá dar algumas informações.
async def info(ctx):
    info = discord.Embed(
        title='Informações',
        description=informacoes,
        colour=11598249
    )
    await ctx.reply(embed=info)

@bot.command() #!rz julgar (@usuário) (motivo) - O bot iniciará um julgamento no servidor. 
async def julgar(ctx, user:discord.Member, *, motivo):
    embed = discord.Embed(title=f'INCIANDO JULGAMENTO',
    description=f'**Réu:** {user}\n**Motivo:** {motivo}.\n**Juiz:** {ctx.author}',
    color=discord.Color.green())

    await ctx.reply(embed=embed)  

@bot.command() #!rz kick (@usuário) - O bot irá kickar o usuário mencionado.
async def kick(ctx:commands.Context, user:discord.Member):
    autor = ctx.author
    if ctx.message.author.guild_permissions.ban_members:
        await ctx.guild.ban(user)
        await ctx.reply(f'O/A {user.display_name} foi kickado(a) desse mundo! Parece que suas ações romperam os laços do espaço-tempo, e agora estão proibidos de interagir em nosso universo.')
    else:
        await ctx.reply(f'{autor} pare de tentar kickar as pessoas! Caso contrário o próximo será você..')

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

@bot.command() #!bk nome - O bot irá gerar um nome aleatório.
async def nome(ctx):
    try: 
        fake = Faker('pt_BR')
        nome = fake.name()
        await ctx.reply(f'{nome} é um ótimo nome!')
    except Exception as e:
        print(f'Erro ao executar o comando {e}')

@bot.command() #!rz piada - O bot irá contar uma piada aleatória sobre Re:Zero.
async def piada(ctx):
    piada = random.choice(piadas)
    await ctx.reply(piada)

@bot.command() #!rz rir - O bot irá rir junto com você.
async def rir(ctx):
    await ctx.message.delete()
    risada = random.choice(risadas)
    if risada == 'rs':
        await ctx.send(risada*(random.randint(1,3)))
    else:
        await ctx.send(((risada+(risadas[random.randint(0,len(risadas)-2)]))*(random.randint(1,5))))

@bot.command() #!rz saudar - O bot irá saudar o usuário.
async def saudar(ctx):
    user = ctx.author
    await ctx.reply(f'> Heya {user.display_name}! Aqui é o Barusu. Retornando pela morte estou aqui para encarar qualquer desafio. A vida é cheia de reviravoltas, mas não se preocupe, estou sempre pronto para recomeçar!')

@bot.command() #!rz total_membros - O bot informará quantos membros tem no servidor.
async def total_membros(ctx):
    servidor = ctx.guild
    total_membros = servidor.member_count
    nome_servidor = servidor.name
    await ctx.send(f'O Mundo {nome_servidor} tem {total_membros} pessoas.')  

@bot.command() #!rz versiculo - O bot irá mandar uma passagem da biblia.
async def versiculo(ctx):
    async with ctx.channel.typing():

        lb = [
            # Abreviação dos livros do AT
            'GN', 'EX', 'LV', 'NM', 'DT', 'JS', 'JZ', 'RT', '1SM', '2SM', '1RS',
            '2RS', '1CR', '2CR', 'ED', 'NE', 'ET', 'JÓ', 'SL', 'PV', 'EC', 'CT', 'IS', 'JR',
            'LM', 'EZ', 'DN', 'OS', 'JL', 'AM', 'OB', 'JN', 'MQ', 'NA', 'HC', 'SF', 'AG', 'ZC', 'ML',
            # Abreviação dos livros do NT
            'MT', 'MC', 'LC', 'JO', 'AT', 'RM', '1CO', '2CO', 'GL', 'EF', 'FP', 'CL', '1TS', '2TS',
            '1TM', '2TM', 'TT', 'FM', 'HB', 'TG', '1PE', '2PE', '1JO', '2JO', '3JO', 'JD', 'AP'
        ]

        teste = 0

        while teste == 0:

            try:
                livro = random.choice(lb)

                if livro == 'SL':
                    cap = random.choice(1,150)
                elif livro == 'IS':
                    cap = random.choice(1,66)
                elif livro == 'JR':
                    cap = random.choice(1,52)
                elif livro == 'GN':
                    cap = random.choice(1,50)
                else:
                    cap = random.randint(1,42)
                if livro == 'SL' and cap == 119:
                    ver = random.randint(1,176)
                elif livro == 'NM' and cap == 7:
                    ver = random.randint(1,89)
                elif livro == 'LC' and cap == 1:
                    ver = random.randint(1,80)
                else:
                    ver = random.randint(1,60)
                    
                response = requests.get(f'https://www.bibliaonline.com.br/TB/{livro}/{cap}/{ver}')
                
                if response.status_code == 200:
                    print(response.text)  # Imprime o HTML da página para inspeção
                    soup = BeautifulSoup(response.text, 'html.parser')
                    versiculo_texto = soup.find('div', class_='verseByVerse css-188hggs')  # Altere para a classe real que contém o texto do versículo
                    if versiculo_texto:
                        embed = discord.Embed(
                            title=f'**Biblia Sagrada** - {livro} {cap}:{ver}\n',
                            description=f'`{versiculo_texto.get_text()}`',
                            color=discord.Color.green())
                        await ctx.reply(embed=embed)
                        teste = 1

            except Exception as e:
                print(f'Erro ao executar o comando: {e}')


@bot.command() #!rz xingar (@usuário)- O bot irá xingar o usuário mencionado
async def xingar(ctx, user:discord.Member):
    xingamento = random.choice(xingamentos)
    frase = [f'O(a) {user.mention} é um(a) {xingamento}',f'{user.mention}, seu {xingamento}!']
    await ctx.reply(random.choice(frase))

@bot.command() #!rz wiki (termo) - O bot vai pesquisar na wikipedia o que o usuário pedir.
async def wiki(ctx: commands.Context, *, termo):
    async with ctx.channel.typing():
        try:
            artigo = termo.replace(" ", "_")
            response = requests.get(f'https://pt.wikipedia.org/wiki/{artigo}')

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                wikipedia = soup.find('div', class_='mw-content-ltr mw-parser-output')
                
                if wikipedia:
                    # Encontra o primeiro parágrafo que contém informações sobre o termo
                    primeiro_paragrafo = wikipedia.find('p', recursive=False)

                    texto_principal = ''
                    if primeiro_paragrafo:
                        # Remove as tags <sup> (superescrito) do texto
                        for sup in primeiro_paragrafo.find_all('sup'):
                            sup.extract()  # Remove a tag <sup> e seu conteúdo

                        texto_principal += primeiro_paragrafo.get_text().strip() + '\n\n'

                        # Verifica se há uma lista não ordenada (<ul>) imediatamente após o primeiro parágrafo
                        ul = primeiro_paragrafo.find_next_sibling('ul')
                        if ul:
                            # Adiciona o conteúdo da lista não ordenada ao texto principal
                            texto_principal += '\n'.join([li.text.strip() for li in ul.find_all('li')]) + '\n\n'

                        embed = discord.Embed(
                            title=f'{termo} na Wiki:',
                            description=texto_principal[:2000],
                            color=discord.Color.green())
                        embed.set_footer(text=f'fonte: https://pt.wikipedia.org/wiki/{artigo}')

                        await ctx.reply(embed=embed)
                    else:
                        await ctx.reply(f'A Wikipédia não possui um artigo com este nome **exato**. Por favor, procure por `{artigo}` na Wikipédia para buscar por títulos alternativos. ')
                else:
                    await ctx.reply(f'A Wikipédia não possui um artigo com este nome **exato**. Por favor, procure por `{artigo}` na Wikipédia para buscar por títulos alternativos. ')
            else:
                await ctx.reply(f'A Wikipédia não possui um artigo com este nome **exato**. Por favor, procure por `{artigo}` na Wikipédia para buscar por títulos alternativos. ')
        except Exception as e:
            print(f'Ocorreu um erro no comando: {e}')

#EVENTOS
@bot.event #Quando alguem escrever uma mensagem que contenha a palavra rem o usuário o responde.
async def on_message(pal:discord.Message):
    await bot.process_commands(pal) #processar se a mensagem era algum comando.
    emoji = random.choice(emojis)

    #tratamento da mensagem.
    frase = pal.content.lower() #toda minúscula
    msg = frase.replace(" ", "") #sem espaços

    #condições
    if pal.author == bot.user:
        return
    if 'rem' in msg:
        await pal.reply('REM??????')
    elif 'loritta' in msg:
        await pal.reply('Ela quer ser a rainha do humor, mas acho que seu código fonte está mais para uma comédia romântica do que para algum algoritmo eficiente :rofl:.')
    elif 'louco' in msg:
        await pal.reply(':clown:')
        await pal.reply('Louco? Eu já fui louco uma vez, eles me deixaram num quarto, num quarto apertado com ratos, isso me deixou louco, louco?')
    elif 'bomdia' in msg:
        await pal.reply(f'Bom diaaa! {emoji}')
    elif 'boanoite' in msg:
        await pal.reply(f'Dorme bem.. {emoji}')
    elif 'boatarde' in msg:
        await pal.reply(f'Boa tarde. {emoji}')

@bot.event #Quando o bot estiver online irá aparecer no console.
async def on_ready():
    print(f'{bot.user} está online!')
    canal = bot.get_channel(757649361248190546)
    await canal.send('Spawnpoint!')

@bot.event #Quando o usuário digitar um comando errado o bot vai lhe informar e lhe sugerir que utilize o comando de ajuda.
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Comando não encontrado. Use `!rz ajuda` para ver a lista de comandos disponíveis.')

#VALIDAR TOKEN
bot.run(TOKEN)
