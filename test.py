from discord.ext import commands
from old_data.yt_dl import download
from old_data.play_command import play_file_from_path_and_leave
import discord
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.command()
async def add(ctx, url):
    await download(url, 'music/' + url[24:])
    await ctx.send(f'Successfully added {url}.mp3 to the download queue.')
    # Обновляем JSON-файл
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

@bot.command()
async def play(ctx):
    # Чтение данных из JSON-файла
    with open('queue.json', 'r') as f:
        data = json.load(f)

    voice_channel_id = str(ctx.author.voice.channel.id)  # Получение ID голосового канала, в котором находится вызывающий
    if voice_channel_id in data:
        file_names = data[voice_channel_id]  # Получение списка файлов из JSON-файла для данного голосового канала
        if file_names:
            await ctx.send(f'The bot is currently playing in the voice channel {ctx.author.voice.channel.name}')
            for file_name in file_names:
                await play_file_from_path_and_leave(ctx, 'music/' + file_name)  # Вывод списка файлов на консоль
                remove_first_file_from_queue(voice_channel_id)
        else:
            await ctx.send('The queue is empty.')
    else:
        await ctx.send('No queue found for the voice channel you are in.')

def remove_first_file_from_queue(voice_channel_id):
    # Чтение данных из JSON-файла
    with open('queue.json', 'r+') as f:
        data = json.load(f)

        if voice_channel_id in data:
            file_names = data[voice_channel_id]
            if file_names:
                file_to_remove = file_names[0]  # Получение имени файла для удаления (первый в очереди)
                file_names.remove(file_to_remove)  # Удаление файла из списка
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                return file_to_remove
            else:
                return None  # Если очередь пуста, возвращаем None
        else:
            return None  # Если ID голосового канала не найден в JSON-файле, возвращаем None

async def stop_playback(ctx):
    voice_client = ctx.voice_client

    if voice_client.is_playing():
        voice_client.stop()  # Остановка воспроизведения
        await ctx.send('Playback stopped.')
    else:
        await ctx.send('No playback to stop.')


@bot.command()
async def skip(ctx):
    voice_channel_id = str(ctx.author.voice.channel.id)
    voice_client = ctx.voice_client

    if voice_client.is_playing():
        voice_client.stop()  # Остановка воспроизведения
        await ctx.send('Song skipped.')
        with open('queue.json', 'r+') as f:
            data = json.load(f)

            if voice_channel_id in data:
                file_names = data[voice_channel_id]
                if file_names:
                    file_to_remove = file_names[0]  # Получение имени файла для удаления (первый в очереди)
                    file_names.remove(file_to_remove)  # Удаление файла из списка
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    return file_to_remove
                else:
                    return None  # Если очередь пуста, возвращаем None
            else:
                return None  # Если ID голосового канала не найден в JSON-файле, возвращаем None
        for file_name in file_names:
            await play_file_from_path_and_leave(ctx, 'music/' + file_name)  # Вывод списка файлов на консоль
    else:
        await ctx.send('No playback to stop.')
    ctx.voice_client.pause()
    await play(ctx)

@bot.command()
async def now_playing(ctx):
    voice_channel = ctx.author.voice.channel
    voice_client = ctx.voice_client

    if voice_client.is_playing():
        await ctx.send(f"The bot is currently playing in the voice channel '{voice_channel.name}'.")
    else:
        await ctx.send("The bot is not currently playing in any voice channel.")

@bot.command()
async def queue(ctx):
    voice_channel_id = str(ctx.author.voice.channel.id)
    with open('queue.json', 'r') as f:
        data = json.load(f)

    if voice_channel_id in data:
        file_names = data[voice_channel_id]
        if file_names:
            await ctx.send(f"Files in queue for voice channel '{ctx.author.voice.channel.name}':")
            for index, file_name in enumerate(file_names, start=1):
                await ctx.send(f"{index}. {file_name}")
        else:
            await ctx.send("The queue is empty.")
    else:
        await ctx.send("No queue found for the voice channel you are in.")

bot.run('MTA5NjQ0NDQ4NjYyNTgwNDM4OA.GH5Igv.Ts7mGGfP3QmZl_6YSqF41gGmf4Rjw-6rLsf5go')