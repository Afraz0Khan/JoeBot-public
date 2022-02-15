import discord
from discord.ext import commands
from weather import weather
from identification import channels, messages
from github import get_gh
from imp_functions import *
from creds import joebot_creds


from os import listdir
from os.path import isfile, join
import time
from reddit import reddit, get_reddit_meme
import json
from help_embed import helpEmbed
from main_functions import *



intents = discord.Intents.default()
intentsForGet = discord.Intents.none()
intents.members = True 
intents.presences = True
intentsForGet.reactions = True
intentsForGet.guilds = True


bot = commands.Bot(command_prefix='$', intents = intents, help_command=None)

@bot.event
async def on_ready(): 

    await bot.get_channel(channels['UAlberta']['logs']).send(f"logged at {time.strftime('%Y-%m-%d | %H:%M:%S',time.localtime(time.time()))}")
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.streaming, name = 'with deez nuts'))

   

    
iAmFeatureList = ["im", "Im" , "IM", "I'm", "i'm", "I'M"]

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if check_f(message):
        await message.channel.send('f')

    if check_link(message):

        logs = discord.utils.find(lambda c: c.name == 'logs', message.guild.channels)

        embed = discord.Embed(
            title = f"{message.author.name} sent the following link in {message.channel.name}:",
            description = message.content,
            color = 0xd1342c
        )

        await logs.send(bot.get_user(650423022317994037).mention, embed = embed)

        await message.delete()


    if message.channel.id == 839092213824618536:
        await add_updownvote(message)

    
    if check_media(message):
       
        await add_updownvote(message)
    


    if message.guild.id == 831855221528985651: 
        role = discord.utils.find(lambda r: r.name == 'afk (avoid pinging)', message.guild.roles)
        if role in message.author.roles:
            await message.author.remove_roles(role)

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


    
    if message.guild.id == 831855221528985651: 
        muted_role = discord.utils.find(lambda r: r.name == 'Muted', message.guild.roles)

        if muted_role in message.author.roles:
            await message.delete()
    

    
    if len(message.content.split(' ')) < 3:
        await manage_dad(message)


    await bot.process_commands(message)




@bot.command()
async def send(ctx, channel_id, *, message):
    if ctx.author.id == 650423022317994037:
        channel_id=int(channel_id)
        await bot.get_channel(channel_id).send(message)
    else:
        await ctx.channel.send('Lol no')





# @bot.command()
# async def ii(ctx, username):
#     result = get_insta(username)

#     if result['biography'] is None or len(result['biography'])==0: result['biography']='N/A'
#     if result['full_name'] is None or len(result['full_name'])==0: result['full_name']='N/A'
#     if result['external_url'] is None: result['external_url']='N/A'
    

#     embed = discord.Embed(
#         title="The instagram profile of " + username, 
#         description = f"@[{username}](https://www.instagram.com/{username})", 
#         color = 0x1FB4DA
#     )
    
#     embed.add_field(name=' `Full Name` ', value=result['full_name'],inline=True)
#     embed.add_field(name=' `Followers` ', value=result['followers_count'],inline=True)
#     embed.add_field(name=' `Following` ', value=result['following_count'],inline=True)
#     embed.add_field(name=' `Bio` ', value=result['biography'],inline=True)
#     embed.add_field(name=' `Total posts` ', value=result['total_posts'],inline=True)
#     embed.add_field(name=' `Country Code` ', value=result['country_code'],inline=True)
#     embed.add_field(name=' `is_private` ', value=result['is_private'],inline=True)
#     embed.set_image(url=result['profile_pic_url_hd'])

#     await ctx.channel.send(embed=embed) 


@bot.command()
async def wr(ctx, location):
    weather_data = weather(str(location))

    embed = discord.Embed(
        title=weather_data["place_name"]+" "+weather_data["temp_now"]+chr(176)+"C",
        description="```"+weather_data["weather_main"]+"```",
        color=0x1FB4DA
        )
        
    embed.set_thumbnail(url = weather_data["icon_url"])

    embed.add_field(name=' `Description` ', value= weather_data["weather_disc"], inline=True)
    embed.add_field(name=' `Feels like` ', value=weather_data["temp_feels"]+chr(176)+"C", inline=True)
    embed.add_field(name=' `Visibility` ', value=weather_data["visibility_info"]+"m", inline=False)
    embed.add_field(name=' `Wind speed` ', value=weather_data["wind_speed"]+"km/h",inline=True)
    embed.add_field(name=' `Cloud cover` ',value=weather_data["cloud_info"]+"%",inline=True)
    embed.add_field(name=' `Pressure` ', value=weather_data["pressure_value"]+"bar",inline=True)
    embed.add_field(name=' `Humidity` ',value=weather_data["humidity_percentage"]+"%",inline=False)
    embed.add_field(name=' `Sunrise time` ',value=weather_data["sunrise_time"]+"am",inline=True)
    embed.add_field(name=' `Sunset time` ',value=weather_data["sunset_time"]+"pm",inline=True)

    await ctx.channel.send(embed=embed)





#done
@bot.command()
async def gp(ctx, member: discord.Member, count: int):

    b_role = discord.utils.find(lambda r: r.name == 'Boosters', ctx.guild.roles)

    if member.id == 650423022317994037:
        embed = discord.Embed(title = '`no`', colour = 0x1FB4DA)
        return await ctx.channel.send(embed=embed)

    if count>50 and ctx.author.id not in {650423022317994037}:
        embed = discord.Embed(title="Please keep the ping count below 100.", colour = 0x1FB4DA)
        return await ctx.channel.send(embed=embed)
    
    if b_role in ctx.author.roles or ctx.author.id in {650423022317994037}:

        await ctx.message.delete()

        for _ in range(count):
            await ctx.channel.send(member.mention, delete_after=0.01)
    
    else:
        embed = discord.Embed(
            title = "You do not have permission to use this command.",
            description = 'This command is reserved for server boosters.\nPlease contact an Admin or a Mod for help.',
            colour = 0x1FB4DA
        )
        await ctx.send(embed = embed)







@bot.command()
async def gh(ctx, username):
    data = get_gh(str(username))

    embed = discord.Embed(
        title = f"{data['name']}",
        description = f"```Username: {data['login']}```\n[Link to profile]({data['html_url']})",
        color = 0x24292e
    )

    embed.set_thumbnail(url= data['avatar_url'])

    embed.add_field(name='`Bio`', value=data['bio'], inline=False)

    embed.add_field(name='`Followers`', value=data['followers'], inline=True)

    embed.add_field(name='`Following`', value=data['following'], inline=True)

    embed.add_field(name='`Public Repos`', 

    value=f"[{data['public_repos']}]({data['html_url'] + '?tab=repositories'})", 

    inline=True)

    embed.add_field(name='`Created at`',value=data['created_at'], inline=False)

    embed.set_footer(text= f"Profile parse time: {data['resp_time']}")

    await ctx.channel.send(embed= embed)







#mod eval
@bot.command()
async def em(ctx, expression):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)

    cmd_access_list = [boost_role, fac_mod, mod_role]

    if not ((ctx.author.id == 650423022317994037) or any([i in ctx.author.roles for i in cmd_access_list])):
        embed = discord.Embed(title = '`You do not have permissions to use this command.`', colour = 0x1FB4DA)
        return await ctx.channel.send(embed=embed)

    elif 'import' not in str(expression):
        try:
            await ctx.channel.send(eval(expression))
            await ctx.message.add_reaction("\N{Ballot Box with Check}")
        except Exception as error:
            embed = discord.Embed(title = '`The following error occurred while processing this command:`', 
            description = f'{error}', colour = 0x1FB4DA)
            return await ctx.channel.send(embed=embed)

    

'''
#user eval(Done: final)
@bot.command()
async def ev(ctx, expression):
    try:
        result = str(eval(expression))
        await ctx.channel.send(result)
    except Exception as error:
        embed = discord.Embed(title = '`The following error occurred while processing this command:`', 
        description = f'{error}', colour = 0x1FB4DA)
        return await ctx.channel.send(embed=embed)
'''



@bot.command()
async def ss(ctx):
    if ctx.author.id in {650423022317994037}:
        onlyfiles = [f for f in listdir('./results') if isfile(join('./results', f))]
        for i in onlyfiles:
            await ctx.channel.send(file = discord.File(f'./results/{i}'))
            time.sleep(1)



@bot.command()
async def r(ctx, subreddit, subreddit_filter = None, post_limit = 1, t_filter = None):
    try: 
        if get_reddit_meme(subreddit, subreddit_filter, post_limit) == False:
            embed = discord.Embed(
                title = 'Please keep the count below or equal to 20',
                colour = 0x1FB4DA
            )
            await ctx.channel.send(embed = embed)

        for i in get_reddit_meme(subreddit, subreddit_filter, post_limit, t_filter):
            await ctx.channel.send(i)
    
    except:
        pass



    

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    if message_id == 846005699581968394:
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'PogChamp':
            role = discord.utils.get(guild.roles, name = 'Gaming pings')

        if role is not None:
            member = payload.member

            if member is not None:
                await member.add_roles(role)
    
    if message_id == 853550933315944458:
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🎥':
            role = discord.utils.get(guild.roles, name = 'MovieNights™️ Partner')

        if role is not None:
            member = payload.member

            if member is not None:
                await member.add_roles(role)
    
    if message_id == 854095093421441044:
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        
        if payload.emoji.name == 'rimuru_hearteyes':
            
            role = discord.utils.get(guild.roles, name = 'Anime nerds')

        if role is not None:
            member = payload.member

            if member is not None:
                await member.add_roles(role)

        




@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    
    if message_id == 846005699581968394:
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'PogChamp':
            role = discord.utils.get(guild.roles, name = 'Gaming pings')

        if role is not None:
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
    
    if message_id == 853550933315944458:
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🎥':
            role = discord.utils.get(guild.roles, name = 'MovieNights™️ Partner')

        if role is not None:
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
    
    if message_id == 854095093421441044:
        guild_id = payload.guild_id

        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'rimuru_hearteyes':
            role = discord.utils.get(guild.roles, name = 'Anime nerds')

        if role is not None:
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
    






@bot.command()
async def av(ctx, *, member: discord.Member):

    embed = discord.Embed(
        description = f"[Link to {member.mention}'s avatar url]({member.avatar_url})",
    )
    embed.set_image(url= member.avatar_url)
    
    await ctx.send(embed = embed)
    

# #afk cmd
# #make a default afk message

@bot.command()
async def afk(ctx, *,custom_message = ''):
    guild = ctx.guild
    
    if int(guild.id) == 831855221528985651:
        
        if ctx.author.nick is None:
            
            await ctx.author.edit(nick = f"{ctx.author.name} [AFK]")
        
        elif ctx.author.nick:
            
            await ctx.author.edit(nick = f"{ctx.author.nick} [AFK]")

        role = discord.utils.find(lambda r: r.name == 'afk (avoid pinging)', guild.roles)
        print(type(role))
        afk_url = ctx.message.jump_url
        

        if custom_message == '':
            custom_message = "No message left"

        embed = discord.Embed(
            title = f"```I've set your status as AFK with the following message:```",
            description = f"[{custom_message}]({afk_url})",
            colour = 0x1FB4DA
        )

        embed.set_thumbnail(url = str(ctx.author.avatar_url))
        
        await ctx.author.add_roles(role)

        await ctx.send(ctx.author.mention, embed = embed)

       
    
@bot.command()
async def pc(ctx, member: discord.Member):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)

    cmd_access_list = [boost_role, fac_mod, mod_role]

    
    if (ctx.author.id == 650423022317994037) or any([i in ctx.author.roles for i in cmd_access_list]):

        if member.raw_status not in 'offline':

            if str(member.desktop_status) not in 'offline':
                await ctx.send(f"{member.mention} is on desktop")
            
            elif str(member.web_status) not in 'offline':
                await ctx.send(f"{member.mention} is on web client 🤮 🤢")

            elif member.is_on_mobile:
                await ctx.send(f"{member.mention} is on mobile 🤮 🤢")
        
        else:
            await ctx.send('The specified member is offline on all their devices')
            



@bot.command()
async def j(ctx, target: discord.Member, *,custom_message = ''):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [boost_role, fac_mod, mod_role]

    if custom_message == '':
        custom_message = 'This is a consequence of a regulation that has been violated by you.'
        
    embed = discord.Embed(
            title = f"`{target.name}` has been jailed by `{ctx.author.name}` with the following message:",
            description = f"{custom_message}",
            color = 0x6f0d0d
        )




    if target.id == 650423022317994037:
        target = ctx.author
        embed = discord.Embed(
            title = "How dare you. This has been notified to Tendi.",
            description = "Wow. You really thought you could outplay the system, didn't you?",
            color = 0x6f0d0d
        )


    if ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):
    
        target_roles = target.roles

        role_list = [str(target_roles[i]) for i in range(0, len(target_roles))]

        filtered_role_list = [item for item in role_list if item not in ['@everyone', 'Boosters']] 

        

        
             

        if 'Jailed' not in filtered_role_list:    
        
            role_obj = {str(target) : filtered_role_list}

            try:
                append_json(role_obj, 'pre_jail_roles.json')
            
            except:
                start_json(role_obj, 'pre_jail_roles.json')
                
            await ctx.send(embed = embed)

            for i in target_roles:
                if str(i) not in ('@everyone', 'Boosters'):
                    if i is not None:
                        role = discord.utils.find(lambda j: j.name == str(i), ctx.guild.roles)

                        await target.remove_roles(role)
            
            jail_role = discord.utils.find(lambda r: r.name == 'Jailed', ctx.guild.roles)
            
            await target.add_roles(jail_role)
    


                
@bot.command()
async def unj(ctx, target: discord.Member):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [boost_role, fac_mod, mod_role]


    if ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):
        target_roles = target.roles

        role_list = [str(target_roles[i]) for i in range(0, len(target_roles))]

        embed = discord.Embed(
            title = f"`{target.name}` has been brought back from the jail by `{ctx.author.name}`.",
            color = 0x1FB4DA
        )
        

        if 'Jailed' in role_list:
            pre_roles = get_jailed_roles(str(target))

            remove_from_json(str(target), 'pre_jail_roles.json')

            for i in pre_roles:
                role = discord.utils.find(lambda j: j.name == str(i), ctx.guild.roles)
                await target.add_roles(role)
            
            jail_role = discord.utils.find(lambda j: j.name == 'Jailed', ctx.guild.roles)
            
            await target.remove_roles(jail_role)
            await ctx.send(embed = embed)





@bot.command()
async def mute(ctx, target: discord.Member):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [boost_role, fac_mod, mod_role]

    embed = discord.Embed(
            title = f"{target.name} has been muted by {ctx.author.name}.",
            description = "Please contact an Admin/Mod if this is a mistake.",
            color = 0x29f24b
        )


    if target.id == 650423022317994037:
        target = ctx.author
        embed = discord.Embed(
            title = f'How dare you `{target.name}``. This has been notified to Tendi.',
            description = 'get fucked lmao'
        )



    if ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):

        
        muted_role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        
        await ctx.send(embed = embed)

        await target.add_roles(muted_role)
        

         

@bot.command()
async def unmute(ctx, target: discord.Member):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [boost_role, fac_mod, mod_role]


    if ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):
    
        embed = discord.Embed(
            title = f"{target.name} has been unmuted by {ctx.author.name}."
        )

        await ctx.send(embed = embed)
        
        muted_role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)

        await target.remove_roles(muted_role)



@bot.command()
async def nick(ctx, *, new_nick):
    
    
    if ctx.author.nick is None:

        await ctx.author.edit(nick = new_nick)

        embed = discord.Embed(
            title = f"{ctx.author.name}'s name was changed.",
            description = f"`{ctx.author.name}` **===>** `{new_nick}`",
            colour = 0x1FB4DA
        )

        embed.set_thumbnail(url= ctx.author.avatar_url)
        await ctx.send(ctx.author.mention, embed = embed)
        
    elif ctx.author.nick:

        previous_nick = ctx.author.nick

        await ctx.author.edit(nick = new_nick)

        embed = discord.Embed(
            title = f"{ctx.author.name}'s name was changed.",
            description = f"`{previous_nick}` **===>** `{new_nick}`",
            colour = 0x1FB4DA
        )


        embed.set_thumbnail(url = ctx.author.avatar_url)


        await ctx.send(ctx.author.mention, embed = embed)


    

# async def remind(ctx, message, time):



@bot.command()
async def backupChannel(ctx, channel_id):
    if ctx.author.id in {650423022317994037}:
        channel = bot.get_channel(int(channel_id))
        msgs = channel.history()
        msg_list = await msgs.flatten()

        await ctx.send(msg_list)
        
# @bot.command()
# async def cn(ctx, aim, new_nick):

#     if ctx.author.id in {650423022317994037}:

#         target = discord.utils.find(lambda r: r.name == )

#         if target.nick is None:

#             await target.edit(nick = new_nick)

#             embed = discord.Embed(
#                 title = f"{target.name}'s name was changed.",
#                 description = f"`{target.name}` **===>** `{new_nick}`",
#                 colour = 0x1FB4DA
#             )

#             embed.set_thumbnail(url= target.avatar_url)
#             await ctx.send(embed = embed)
            
#         elif target.nick:

#             previous_nick = target.nick

#             await target.edit(nick = new_nick)

#             embed = discord.Embed(
#                 title = f"{target.name}'s name was changed.",
#                 description = f"`{previous_nick}` **===>** `{new_nick}`",
#                 colour = 0x1FB4DA
#             )


#             embed.set_thumbnail(url = target.avatar_url)


#             await ctx.send(embed = embed)
    
    
    
# @bot.command()
# async def test(ctx):
#     embed = discord.Embed(
#         title = 'joemama'
#     )
    
#     embed.set_thumbnail(url="attachment://ABHIMANYU DAYAL.png")
#     await ctx.send(embed = embed)




@bot.command()
async def result(ctx):
    if ctx.author.id in {650423022317994037}:
        with open('result.json', 'r+') as file:
            data = json.load(file)
            keys = list(data.keys())


            for i in keys:

                eng = data[i]["ENGLISH CORE"]
                math = data[i]["MATHEMATICS"]
                phy = data[i]["PHYSICS"]
                chem = data[i]["CHEMISTRY"]
                cs = data[i]["COMPUTER SCIENCE (NEW)"]

                percentage = (int(eng['total'])+int(math['total'])+int(phy['total'])+int(chem['total'])+int(cs['total']))/5
                color = ''
                if percentage <88:
                    color = 0xf54242
                elif percentage <91:
                    color = 0xf58742
                elif percentage < 93:
                    color = 0xf5b342
                elif percentage < 100:
                    color = 0xe3f542

                embed = discord.Embed(
                    title = f"CBSE board result of **{i}**",
                    description = f"Congrats on scoring a whopping **{percentage}%**",
                    color = color
                )
                
                file = discord.File(f'./results/{i.upper()}.png')

                embed.add_field(name= f'Subject-1:',value= '```English```', inline=False)
                embed.add_field(name= f'**Theory**', value= eng['theory'], inline=True)
                embed.add_field(name=f'**Practical**', value=eng['prac'], inline=True)
                embed.add_field(name=f'**Grade**', value=eng['grade'], inline=True)
                embed.add_field(name=f'**Total**', value=(int(eng['theory'])+int(eng['prac'])),inline=True)
                


                embed.add_field(name= f'Subject-2:',value= '```Math```', inline=False)
                embed.add_field(name= f'**Theory**', value= math['theory'], inline=True)
                embed.add_field(name=f'**Practical**', value=math['prac'], inline=True)
                embed.add_field(name=f'**Grade**', value=math['grade'], inline=True)
                embed.add_field(name=f'**Total**', value=(int(math['theory'])+int(math['prac'])),inline=True)

                time.sleep(0.2)

                embed.add_field(name= f'Subject-3:',value= '```Physics```', inline=False)
                embed.add_field(name= f'**Theory**', value= phy['theory'], inline=True)
                embed.add_field(name=f'**Practical**', value=phy['prac'], inline=True)
                embed.add_field(name=f'**Grade**', value=phy['grade'], inline=True)
                embed.add_field(name=f'**Total**', value=(int(phy['theory'])+int(phy['prac'])),inline=True)


                embed.add_field(name= f'Subject-4:',value= '```Chemistry```', inline=False)
                embed.add_field(name= f'**Theory**', value= chem['theory'], inline=True)
                embed.add_field(name=f'**Practical**', value=chem['prac'], inline=True)
                embed.add_field(name=f'**Grade**', value=chem['grade'], inline=True)
                embed.add_field(name=f'**Total**', value=(int(chem['theory'])+int(chem['prac'])),inline=True)


                embed.add_field(name= f'Subject-5:',value= '```Computer Science```', inline=False)
                embed.add_field(name= f'**Theory**', value= cs['theory'], inline=True)
                embed.add_field(name=f'**Practical**', value=cs['prac'], inline=True)
                embed.add_field(name=f'**Grade**', value=cs['grade'], inline=True)
                embed.add_field(name=f'**Total**', value=(int(cs['theory'])+int(cs['prac'])),inline=True)

                time.sleep(0.5)

                await ctx.channel.send(file = file, embed = embed)

                time.sleep(0.5)

                


@bot.command()
async def vct(ctx):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [boost_role, fac_mod, mod_role]

    if ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):
        vc_category = bot.get_channel(831855221528985653)
        await vc_category.edit(position = 3)
        await ctx.message.add_reaction("\N{Ballot Box with Check}")



@bot.command()
async def unvct(ctx):
    boost_role = discord.utils.find(lambda b: b.id == 852807867274887230, ctx.guild.roles)
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [boost_role, fac_mod, mod_role]


    if ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):
        vc_category = bot.get_channel(831855221528985653)
        await vc_category.edit(position = 12)
        await ctx.message.add_reaction("\N{Ballot Box with Check}")





@bot.command(no_pm = True)
async def help(ctx):
    
    await ctx.send(embed = helpEmbed)




@bot.command()
async def lvs(ctx, server_id):
    if ctx.author.id in {650423022317994037}:
        h = bot.get_guild(int(server_id))
        await ctx.message.add_reaction("\N{Ballot Box with Check}")
        await h.leave()
        

# @bot.command()
# async def sb(ctx):
#     await ctx.send(ctx.guild.banner_url)
#     await ctx.message.add_reaction("\N{Ballot Box with Check}")


# @bot.command()
# async def ssb(ctx, url):
#     await ctx.guild.edit(banner = url)
#     await ctx.message.add_reaction("\N{Ballot Box with Check}")

# @bot.command()
# async def ssi(ctx, url):
#     await ctx.guild.edit(icon = url)
#     await ctx.message.add_reaction("\N{Ballot Box with Check}")
    
    


@bot.command()
async def move(ctx, vc1, vc2=''):
    
    fac_mod = discord.utils.find(lambda f: f.id == 875392679737958432, ctx.guild.roles)
    mod_role = discord.utils.find(lambda r: r.id == 831862902733406238, ctx.guild.roles)
    
    cmd_access_list = [fac_mod, mod_role]

    if ctx.author.id in {650423022317994037} and vc2 == '':
        member = discord.utils.find(lambda r:r.id == int(vc1), ctx.guild.members)
        await member.move_to(None)
        await ctx.message.add_reaction("\N{Ballot Box with Check}")


    elif ctx.author.id in {650423022317994037} or any([i in ctx.author.roles for i in cmd_access_list]):

        channel1 = discord.utils.find(lambda r: r.id == int(vc1), ctx.guild.channels)
        channel2 = discord.utils.find(lambda r: r.id == int(vc2), ctx.guild.channels)

        members = channel1.members
        for i in members:
            await i.move_to(channel2)

        await ctx.message.add_reaction("\N{Ballot Box with Check}")






@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):

    if ctx.author.id in {650423022317994037}:
        await member.kick(reason=reason)
        await ctx.message.add_reaction("\N{Ballot Box with Check}")



@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):

    if ctx.author.id in {650423022317994037}:
        
        await member.ban(reason=reason)
        await ctx.message.add_reaction("\N{Ballot Box with Check}")









bot.run(joebot_creds['token'])
