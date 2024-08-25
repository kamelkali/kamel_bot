import discord
from discord import app_commands
import datetime
from discord.ext import tasks, commands
import asyncio
from client import client, tree
from discord.ui import Button, View
from discord import ButtonStyle

intents = discord.Intents.all()
intents.messages = True


@tree.command(    #tree comands its like slash command (very hard to code)
    name="join",
    description="bot joins the voice channel",
    guild=discord.Object(id=1042652024598167552)
)
async def join(guild_id: int, channel_id: int):
    guild = client.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print('im here')
        except Exception as e:
            print(f'nuh uh: {e}')
    else:
        print('not fund ')

@tree.command(    #tree comands its like slash command (very hard to code)
    name="play",
    description="Play som musik",
    guild=discord.Object(id=1042652024598167552)
)
async def play(interaction: discord.Interaction,url : str): #not sure about url
    if not interaction.user.voice:
        await interaction.response.send_message("womp womp connect to channel my boy")
        return
    play_embed = discord.Embed(title=f"Playing {song_title}", description=f"Playing {url}", color=discord.Color.green())

    view = View()
    pause_button = Button(label="Pause", style=ButtonStyle.primary)
    resume_button = Button(label="Resume", style=ButtonStyle.primary)
    stop_button = Button(label="Stop", style=ButtonStyle.danger)

    async def pause_callback(interaction: discord.Interaction):
        pause_embed = discord.Embed(title=f"Paused {song_title}", description="Paused the music", color=discord.Color.orange())
        await interaction.response.send_message(embed=pause_embed)

    async def resume_callback(interaction: discord.Interaction):
        pause_embed = discord.Embed(title=f"Resumed {song_title}", description="Resumend", color=discord.Color.blue())
        await interaction.response.send_message(embed=pause_embed)

    async def stop_callback(interaction: discord.Interaction):
        stop_embed = discord.Embed(title=f"Stopped {song_title} ", description="Music is stopped", color=discord.Color.red())
        await interaction.response.edit_message(embed=stop_embed, view=None)

    pause_button.callback = pause_callback
    resume_button.callback = resume_callback
    stop_button.callback = stop_callback

    view.add_item(pause_button)
    view.add_item(resume_button)
    view.add_item(stop_button)

    await interaction.response.send_message(embed=play_embed, view=view)
