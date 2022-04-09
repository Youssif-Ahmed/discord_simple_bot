
from os import name, replace
from pickle import TRUE
from types import MemberDescriptorType
import discord
from discord import channel
from discord import message
from discord import user
from discord import guild
from discord.abc import User
from discord import message
from discord.ext import commands
import modulefinder
import random
import asyncio
import string
import math
import typing
import random as r
from discord.ext import tasks 
import time
import nacl
from discord.guild import Guild
import logging



TOKEN ='Token goes here'

bot =discord.Client()
bot = commands.Bot(command_prefix=";",case_insensitive=True)
bot.remove_command("help")

curse =['']


@bot.event
async def on_ready():
    print('""""""""""""""""""""""""""""""""""""""""""""')
    print(f"Bot Connected To The Server As {bot.user} ")
    print('""""""""""""""""""""""""""""""""""""""""""""')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(';help'))

    

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')






#tells you latency
@bot.command()
async def latency(ctx):
    await ctx.send(f'Latency Is {round(bot.latency*100)} ms')








#kicks members
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, why=None):
    if ctx.author == member:
        await ctx.send ('You Cant kick yourself')
        return
    await member.kick(reason=why)
    await ctx.channel.send(f"**{member} has been kicked from this server by {ctx.author} for {why} **")
    channel = bot.get_channel(869239741898444890)
    await channel.send(f'Admin {ctx.    author} kicked {member}')

@kick.error 
async def on_kick_error(ctx,error): 
    if isinstance(error , commands.MissingPermissions):
        await ctx.send ('You Are Not Allowed To Use This Command!')
        await message.delete()


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None , reason = None ):
    if member == ctx.author:
        await ctx.send(f'You Cant Ban Yourself {ctx.author.mention}')
        return
    if member == None:
        await ctx.send(f'Please Mention a User To ban {ctx.author.mention}')
    if reason == None:
        reason = 'No Reason'

    await member.ban(reason=reason)
    await ctx.send(f'User {member} Has Been Banned By {ctx.author} for ({reason})')
    channel = bot.get_channel(869239741898444890)
    await channel.send(f'Admin {ctx.author} Banned {member} for ({reason})')     
                       


@ban.error

async def on_ban_error(ctx,error , message):
    if isinstance(error , commands.MissingPermissions):
        await ctx.send ('You Are Not Allowed To Use This Command!')
        await message.delete()





    
#mute members

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member , reason:str = None):
    role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
    if not role_muted:
        role_muted = await ctx.guild.create_role(name='Muted' , colour=discord.Colour.darker_gray())
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(role_muted, speak=False, mute = True,  send_messages=False, read_message_history=True, read_messages=True)
            await member.add_roles(role_muted)
    elif role_muted:
        await member.add_roles(role_muted)
    await ctx.send(f"User {member.mention} Was Muted By {ctx.author} for {reason}")
    channel = bot.get_channel(869239741898444890)
    await channel.send(f"{ctx.author} Muted {member} for {reason}")






#unmutes members

@bot.command()
@commands.has_role('OWNER')
async def unmute(ctx , member: discord.Member):
    role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role_muted)
    await ctx.send(f"{ctx.author.name} Unmuted {member}")
    channel = bot.get_channel(869239741898444890)
    await channel.send(f"{ctx.author} Unmuted {member}")
    






  


#tells you a joke
@bot.command()
async def joke(message):
    username = str(message.author)
    await message.channel.send(f"{message.author.mention} Is One")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f'Bot Joined room {channel}')

@bot.command()
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send(f'Bot have been disconnected by {ctx.author.mention}')


@bot.command()
@commands.has_role('OWNER')
async def m(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=True)
    await ctx.send('Members have been muted')

@bot.command()
@commands.has_role('....')
async def u(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)
    await ctx.send('Members have been unmuted')

@u.error
async def on_u_error(ctx , error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send('You can do have permission to do that.')
        return



#gives you a ranndom number
@bot.command()
async def random(ctx):
    response= f'this is your random number: {r.randrange(1000000)}'
    await ctx.send (response)



@bot.command()
@commands.has_permissions(administrator=True)
async def bc(ctx, *, message:str = None):
    bcchannel2 = discord.utils.get(ctx.guild.channels, name = 'broadcast')
    logchannelid = 869239741898444890
    logchannel = bot.get_channel(logchannelid)

    if message == None:
        await ctx.send(f'Add a Message For Me To BroadCast {ctx.author.mention}')
        return
    await bcchannel2.send(f'New Bc ------> {message}')
    await logchannel.send(f'**> {ctx.author} Sent a Bc\n> In {bcchannel2.mention}\n> and said    "{message}"\n> in {ctx.guild.name}**')


@bc.error
async def on_bc_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Are Not Allowed To Use This Command")
        return








@bot.command()
async def delrole(ctx, role: discord.Role):
    await role.delete()
    await ctx.send(f' Role "{role}" Has Been Deleted By {ctx.author}')
    delrole_log = discord.utils.get(ctx.guild.channels, name = 'logs')
    await delrole_log.send(f'**Admin {ctx.author} Deleted Role "{role}"**')



@bot.command()
async def help(ctx):
    await ctx.send("""
    ```
    YB bot is here for help!
    the command prefix is ";"
    ;ping ----------------> Pong!
    ;latency ----------------> tells you bot latency
    ;random ----------------> gives you a random number
    ;joke ----------------> Tells You a Joke ;)
--------------------------------------------------------------------

For Admins:
#ban @User you wanna ban , time in days , reason
#kick @user you wanna kick , reason

    when you say hello the bot will respond to you
    when you say bye the bot will respond to you                     
    Thats it for now the bot is under development
    ```                            
    """)

@bot.event
async def on_member_join(ctx, member: discord.Member):
    welcome =discord.utils.get(ctx.guild.channels, name = 'welcome')
    await welcome.send(f'Hello {member.mention} Welcome t{ctx.guild.name}')


@bot.event
async def on_guild_join(ctx):
    channel = bot.get_channel(869239741898444890)
    await channel.send(f'{bot.user} has been added to {ctx.guild.name}')
    



@bot.event 
async def on_message(message):
    username = str(message.author.name)
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message}  ({channel})')

    if message.author == bot.user:
        return
    if message.channel.name == channel: 
       if user_message.lower() == 'hello':
           await message.channel.send(f'Hello {message.author.mention}')    
       elif user_message.lower() == 'bye':
            await message.channel.send(f'See You Later {message.author.mention}')

       elif user_message.lower() == 'ping':
           await message.channel.send('Pong!')

       elif  any (word in user_message.lower() for word in curse):
           await message.channel.send(f'Behave!! {message.author.mention}')
           await message.delete()
           channel = bot.get_channel(869239741898444890)
           await channel.send(f'User {message.author} sent :   {user_message}')
    await bot.process_commands(message)
    return



#note necessary just used it to see the error clearly
@bot.event
async def on_command_error(ctx, error):
  await ctx.send(error)
  raise error
  





bot.run(TOKEN)
