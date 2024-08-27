import asyncio
import discord

from client import client, tree
from yt_dlp import YoutubeDL
from discord import app_commands
from client import client, tree
from discord.ext import commands
from discord.ext.commands import Bot

intents = discord.Intents.all()
intents.messages = True

is_playing = False
is_paused = False
queue = []
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -reconnect_at_eof 1',
    'options': '-vn -ar 48000 -b:a 192k'}

voice_channel = None


def find_music(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(item, download=False)
            if "entries" in info:
                info = info['entries'][0]
        except Exception as e:
            print(f"Error finding music: {e}")
            return False

        url = info.get('url', None)
        if not url:
            formats = info.get('formats', [])
            if formats:
                url = formats[0].get('url', None)

        if not url:
            print("No valid URL found in the info dictionary")
            return False

        return {'source': info, 'title': info['title'], 'url': url, 'thum': info['thumbnail'],
                'duration': info['duration'], 'channel': info['uploader']}


async def play_next(interaction: discord.Interaction):
    global is_playing, queue
    print(f"Queue before playing next: {[song[0]['title'] for song in queue]}")

    if len(queue) > 0:
        is_playing = True
        last_song = queue.pop(-1)
        next_song = queue.insert(0, last_item)
        print(f"Queue after popping song: {[song[0]['title'] for song in queue]}") 
        my_url = next_song[0]['source']['url']
        print(f"Playing next song: {next_song[0]['title']}")

        if not interaction.guild.voice_client or not interaction.guild.voice_client.is_connected():
            target_channel = next_song[1]
            await target_channel.connect()

        try:
            audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            interaction.guild.voice_client.play(audio_source, after=lambda e: after(interaction, e))
            await interaction.followup.send(f"Now playing: {next_song[0]['title']}")
        except Exception as e:
            print(f"Error playing next song: {e}")
            await interaction.followup.send("Error playing the next song")
            is_playing = False
            return

        await play_music(interaction)
    else:
        is_playing = False
        await interaction.followup.send("Queue is empty")

    if len(qeue) > 20:
        queue = queue[:20]
        interaction.response.send_message("Queue is full, only 20 songs can be added")


def playemb(song_title, interaction, song_thum, song_dur, voice_channel, yt_channel):
    view = discord.ui.View()
    play_embed = discord.Embed(title=f"Playing:",
                               description=f"> **Title:** {song_title}\n  > **Duration:** {song_dur}\n  > **By:** {yt_channel}\n > **Playing on:** <#{voice_channel.id}>",
                               color=discord.Color.green())
    play_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
    play_embed.set_thumbnail(url=song_thum)
    play_embed.set_footer(text="coded by kamel⭐")

    pause_button = discord.ui.Button(label="Pause", style=discord.ButtonStyle.primary)
    resume_button = discord.ui.Button(label="Resume", style=discord.ButtonStyle.primary)
    stop_button = discord.ui.Button(label="Stop", style=discord.ButtonStyle.danger)
    skip_button = discord.ui.Button(label="Skip", style=discord.ButtonStyle.primary)

    async def pause_callback(interaction: discord.Interaction):
        await pause(interaction)
        pause_embed = discord.Embed(title=f"Paused song", description="Paused the music",
                                    color=discord.Color.orange())
        await interaction.response.edit_message(embed=pause_embed)

    async def resume_callback(interaction: discord.Interaction):
        await resume(interaction)
        pause_embed = discord.Embed(title=f"Resumed song", description="Resumend",
                                    color=discord.Color.blue())
        stop_button.style = discord.ButtonDisabled
        await interaction.response.edit_message(embed=pause_embed)

    async def stop_callback(interaction: discord.Interaction):
        await stop_song(interaction)
        stop_embed = discord.Embed(title=f"Stopped song ", description="Music stopped",
                                   color=discord.Color.red())
        await interaction.response.edit_message(embed=stop_embed)

    async def skip_callback(interaction: discord.Interaction):
        await skip(interaction)
        stop_embed = discord.Embed(title=f"Skipped  song", description="Skipped the music",
                                   color=discord.Color.red())
        await interaction.response.edit_message(embed=stop_embed)

    pause_button.callback = pause_callback
    resume_button.callback = resume_callback
    stop_button.callback = stop_callback
    skip_button.callback = skip_callback

    view.add_item(pause_button)
    view.add_item(resume_button)
    view.add_item(stop_button)
    view.add_item(skip_button)
    return interaction.response.send_message(embed=play_embed, view=view)


def after(interaction, error):
    try:
        print("Załączono funkcję after")
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.stop()
        asyncio.run_coroutine_threadsafe(play_next(interaction), client.loop)
    except Exception as e:
        print(f"Error in after function: {e}")


async def play_music(interaction: discord.Interaction):
    global is_playing, url, queue, voice_channel
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10 -reconnect_at_eof 1',
        'options': '-vn -ar 48000 -b:a 192k'}

    is_playing = True
    next_song = queue.pop(0)
    url = next_song[0]['url']
    target_channel = next_song[1]

    if voice_channel is None or interaction.guild.voice_client is None or not interaction.guild.voice_client.is_connected():
        voice_channel = await target_channel.connect()
        if voice_channel is None:
            await interaction.response.send_message("Failed to join the channel")
    else:
        await interaction.guild.voice_client.move_to(target_channel)

    if interaction.guild.voice_client is not None:
        audio_source = discord.FFmpegPCMAudio(url, before_options=ffmpeg_options['before_options'],
                                              options=ffmpeg_options['options'])
        interaction.guild.voice_client.play(audio_source, after=lambda e: after(interaction, e))
    else:
        await interaction.response.send_message("Bot is not connected to a voice channel")


async def stop_song(interaction: discord.Interaction):
    if voice_channel.is_playing():
        is_playing = False
        is_paused = True
        voice_channel.pause()
    elif voice_channel.is_paused:
        is_playing = True
        is_paused = False
        voice_channel.resume()


async def resume_song(interaction: discord.Interaction):
    if is_paused:
        is_playing = True
        is_paused = False
        voice_channel.resume()


def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()
        play_next(interaction)


@tree.command(
    name="play",
    description="Play",
)
@commands.cooldown(1, 2, commands.BucketType.user)
async def play(interaction: discord.Interaction, query: str):
    global is_playing, is_paused, queue, voice_channel
    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message("Connect to a voice channel")
        return
    voice_channel = interaction.user.voice.channel
    if is_paused:
        voice_channel.resume()
    else:
        song = find_music(query)
        if not song:
            await interaction.response.send_message(
                "Could not download the song. Incorrect format try another keyword !")
            return
        else:
            song_title = song['title']
            song_thum = song['thum']
            yt_channel = song['channel']
            dur_sec = song['duration']
            song_dur = f"{dur_sec // 60}m:{dur_sec % 60}s"
            await playemb(song_title, interaction, song_thum, song_dur, voice_channel, yt_channel)
            queue.append([song, voice_channel])
        if not is_playing:
            await play_music(interaction)
            queue.append([song, voice_channel])


@tree.command(
    name="stop",
    description="P",
)
async def stop(interaction: discord.Interaction):
    await stop_song(interaction)


@tree.command(
    name="resume",
    description="Resume the music",
)
async def resume(interaction: discord.Interaction):
    await resume_song(interaction)


@tree.command(
    name="skip",
    description="Skip the music",
)
async def skip(interaction: discord.Interaction):
    await stop_song(interaction)


@tree.command(
    name="queue",
    description="Show the music queue",
)
async def show_queue(interaction: discord.Interaction):
    retval = ""

    for i in range(0, len(queue)):
        if i > 4: break
        retval += f"{i + 1}. {queue[i][0]['title']}\n"

    if retval != "":
        await interaction.response.send_message(retval)
    else:
        await interaction.response.send_message("No music in queue")


@tree.command(
    name="clear",
    description="Clear the music queue",
)
async def clear(interaction: discord.Interaction):
    if len(music_queue) > 0 and is_playing:
        voice_channel.stop()
        is_playing = False
        is_paused = False
    music_queue = []
    await interaction.response.send_message("Cleared the queue")


@tree.command(
    name="leave",
    description="Leave the voice channel",
)
async def leave(interaction: discord.Interaction):
    if voice_channel.is_connected():
        is_playing = False
        is_paused = False
        music_queue = []
        await voice_channel.disconnect()

        await interaction.response.send_message("Left the channel")
    else:
        await interaction.response.send_message("I am not in a voice channel")
