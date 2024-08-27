import discord
from discord import app_commands
import datetime
from discord.ext import tasks, commands
import asyncio

intents = discord.Intents.all()
intents.messages = True

client = commands.Bot(
    intents=intents,
    command_prefix="/",
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, replied_user=False)

)
tree = client.tree
