import discord
from discord import app_commands
import datetime
from discord.ext import tasks, commands
import asyncio
from client import client, tree

@tree.command(
    name="ban",
    description="Bans a user (admin only)",
)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "no reason "):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("nuh uh pk said no", ephemeral=True)
        return
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been banned for: {reason}")


@tree.command(
    name="kick",
    description="Kicks a user (admin only)",
)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("pk said no.", ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.mention} has been kicked for: {reason}")


@tree.command(
    name="timeout",
    description="Times out a user (admin only)",
)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int,
                  reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("nuh uh", ephemeral=True)
        return
    await member.timeout(duration=duration, reason=reason)
    await interaction.response.send_message(f"{member.mention} has been timed out for {duration} seconds for: {reason}")
