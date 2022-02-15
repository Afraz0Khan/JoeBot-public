import discord
from identification import channels




def check_f(message):
    if message.content.lower() == 'f':
        return True


def check_link(message):
    if any([key in message.content.lower() for key in ['https://discord.gg/invite/', 'https://discord.gg/','https://www.discord.gg/','https://www.discord.gg/invite']]) and message.author.id not in {650423022317994037}:
        return True


def check_media(message):
    if message.channel.id in channels['UAlberta']['mediaVoteChannelIDs'] and (len(message.attachments)>0 or (('https://' in message.content) and ('https://discord.com' not in message.content))):
        return True



def check_afk(message):
    role = discord.utils.find(lambda r: r.name == 'afk (avoid pinging)', message.guild.roles)
    if role in message.author.roles:
        return True, role


async def manage_afk(role, message):
    try:
        new_nick = message.author.nick.replace('[AFK]', '')
        await message.author.edit(nick = new_nick)
    except:
        pass

    embed = discord.Embed(
        title = f"Welcome back `{message.author}`",
        description = "I've removed your AFK",
        colour = 0x1FB4DA
        )

    await message.channel.send(embed = embed)


async def manage_dad(message):
    iAmFeatureList = ["im", "Im" , "IM", "I'm", "i'm", "I'M"]
    iAmBoolList = [i in iAmFeatureList for i in message.content.split()]
    
    if any(iAmBoolList):
        lst = message.content.split(' ')

        ind = iAmBoolList.index(True)

        rest_lst = lst[ind+1:]

        await message.channel.send(f"hi {' '.join(rest_lst)}, im dad.")



async def add_updownvote(message):
    await message.add_reaction('<:upvote:837037482541449236>')
    await message.add_reaction('<:downvote:837037326885715999>')



