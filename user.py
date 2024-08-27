import discord
from discord import app_commands
import datetime
from discord.ext import tasks, commands
import asyncio
from client import client, tree

intents = discord.Intents.all()
intents.messages = True

@tree.command(
    name="hello",
    description="just simple hello command",
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"sup {interaction.user.mention}")


@tree.command(
    name="ping",
    description="Displays the bot's latency in milliseconds",
)
async def ping(interaction: discord.Interaction):
    latency = client.latency * 1000  # to ms
    if latency < 100:
        status = "Good 🟢"
    elif latency < 200:
        status = "Average 🟠"
    else:
        status = "Bad 🔴"

    await interaction.response.send_message(f"**Latency:** {latency:.2f} ms **Status:** {status}")

@tree.command(    #tree comands its like slash command (very hard to code)
    name="embed",
    description="Creates embeds (admin only)",
)
async def embed(interaction: discord.Interaction, title: str, description: str,color:  str):
    color = discord.Color.from_str(color)
    embed_base = discord.embeds.Embed(title=title, description=description, color=color)
    embed_base.set_footer(text="coded by kamel! ⭐")
    embed_base.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
    await interaction.response.send_message(embed=embed_base)

@tree.command(
    name="pfp",
    description="display other pfp",

)
async def pfp(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        await interaction.response.send_message("nuh uh duddee")
        return

    user_avatar_url = member.display_avatar.url
    await interaction.response.send_message(f"** @{member.name} pfp:** {user_avatar_url}")
