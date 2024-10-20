import discord
import mod
import user
import datetime
import asyncio
import music

from discord import app_commands
from discord.ext import tasks, commands
from client import client, tree
from discord.utils import get



intents = discord.Intents.all()
intents.messages = True

@client.event
async def on_member_join(member):
    channel = guild.system_channel
    if channel.permissions_for(guild.me).send_messages:
        await channel.send(f"Thank You for joining {member.mention}")

@client.event
async def on_member_remove(member):
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
    try:
        await client.wait_until_ready()
        await tree.sync()
        print("Tree sync")
    except Exception as e:
        print(f"Error syncing tree: {e}")
    print('------------------------------')
    print('Launched bot!:')
    print("Bot name:",client.user.name)
    print("Bot ID:",client.user.id)
    print("Launched", datetime.datetime.now())
    print('------------------------------')

client.run('')
