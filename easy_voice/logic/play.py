import discord
import json
import asyncio

async def play(self, ctx):
    with open('queue.json', 'r') as f:
        data = json.load(f)
    ID = str(ctx.author.voice.channel.id)
    if ID in data:
        if data[ID]:
            await ctx.send(f'The bot is currently playing in the voice channel {ctx.author.voice.channel.name}')
            for file_name in data[ID]:
                await play_file_from_path_and_leave(ctx, 'music/' + file_name)
                await remove_first_file_from_queue(ID)
        else:
            await ctx.send('The queue is empty.')
    else:
        await ctx.send('No queue found for the voice channel you are in.')

async def play_file_from_path_and_leave(ctx, path):
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

async def remove_first_file_from_queue(ID):
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
