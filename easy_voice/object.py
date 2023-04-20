import discord
import json
import asyncio
import subprocess
import os.path
from discord.ext import commands
class Kuzmich:
    def __init__(self):
        self.bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
    async def play(self, ctx):
        with open('queue.json', 'r') as f:
            data = json.load(f)
        ID = str(ctx.author.voice.channel.id)
        if ID in data:
            if data[ID]:
                await ctx.send(f'The bot is currently playing in the voice channel {ctx.author.voice.channel.name}')
                for file_name in data[ID]:
                    await self.play_file_from_path_and_leave(ctx, 'music/' + file_name)
                    await self.remove_first_file_from_queue(ID)
            else:
                await ctx.send('The queue is empty.')
        else:
            await ctx.send('No queue found for the voice channel you are in.')
    async def play_file_from_path_and_leave(self, ctx, path):
        if ctx.author.voice.channel is None:
            await ctx.send("Вы должны находиться в голосовом канале, чтобы использовать эту команду.")
            return
        voice_client = await ctx.author.voice.channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 1.0
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()
    async def remove_first_file_from_queue(self, ID):
        with open('queue.json', 'r+') as f:
            data = json.load(f)

            if ID in data:
                file_names = data[ID]
                if file_names:
                    file_to_remove = file_names[0]
                    file_names.remove(file_to_remove)
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    return file_to_remove
                else:
                    return None
            else:
                return None
    async def add(self, ctx, url):
        if os.path.isfile("music/" + url[24:] + '.mp3'):
            await ctx.send(f'Successfully added {url}.mp3 to the download queue.')
            with open('queue.json', 'r+') as f:
                data = json.load(f)
                voice_channel_id = str(ctx.author.voice.channel.id)
                file_name = url[24:] + '.mp3'
                if voice_channel_id in data:
                    data[voice_channel_id].append(file_name)
                else:
                    data[voice_channel_id] = [file_name]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            await self.download(url, 'music/' + url[24:])
            await ctx.send(f'Successfully added {url}.mp3 to the download queue.')
            with open('queue.json', 'r+') as f:
                data = json.load(f)
                voice_channel_id = str(ctx.author.voice.channel.id)
                file_name = url[24:] + '.mp3'
                if voice_channel_id in data:
                    data[voice_channel_id].append(file_name)
                else:
                    data[voice_channel_id] = [file_name]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
    async def download(self, url, destination):
        cmd = f'yt-dlp -x -o "{destination}.mp3" --audio-format mp3 {url}'
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
    async def queue(self, ctx):
        voice_channel_id = str(ctx.author.voice.channel.id)
        with open('queue.json', 'r') as f:
            data = json.load(f)

        if voice_channel_id in data:
            file_names = data[voice_channel_id]
            if file_names:
                temp = f"Files in queue for voice channel '{ctx.author.voice.channel.name}':\n"
                for index, file_name in enumerate(file_names, start=1):
                    temp += f"{index}. {file_name}\n"
                await ctx.send(temp)
            else:
                await ctx.send("The queue is empty.")
        else:
            await ctx.send("No queue found for the voice channel you are in.")
    async def skip(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await voice_client.disconnect()
            await ctx.send('Song skipped.')
        else:
            await ctx.send('No playback to stop.')