import discord
from discord import app_commands
import datetime
from discord.ext import tasks, commands
import asyncio
from client import client, tree
from discord.utils import get

intents = discord.Intents.all()
intents.messages = True

import mod
import user

@client.event
async def on_member_join(member):
    guild = member.guild
    channel = guild.system_channel #system channel (welcome channel)
    if channel.permissions_for(guild.me).send_messages: #making sure you have permissions to send message
        await channel.send(f"Thank You for joining {member.mention}  to **pk research lab**!")

@client.event
async def on_member_remove(member):
    guild = member.guild
    channel = guild.system_channel
    if channel.permissions_for(guild.me).send_messages:
        await channel.send(f"{member.mention} has left the server :(") #same


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(f"hello {message.author.mention} im sleepy rn ")
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if ctx.message.content.count('/') <= 1:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("hhhel naaah")
        else:
            await ctx.send(error)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Cooking beats in FLStudio!"), status=discord.Status.online)
    await tree.sync(guild=discord.Object(id=1042652024598167552))

    guild = client.get_guild(1042652024598167552)
    channel = guild.get_channel(1275178586529206272)

    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print('Connected to voice channel')
        except Exception as e:
            print(f'Failed to connect to voice channel: {e}')
    else:
        print('Voice channel not found or invalid')

    print('------------------------------')
    print('Launched bot! :')
    print("Bot name:",client.user.name)
    print("Bot ID:",client.user.id)
    print("Launched", datetime.datetime.now())
    print('------------------------------')

client.run('TOKEN')
