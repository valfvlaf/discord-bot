import os
import json
import subprocess
import asyncio

async def add(self, ctx, url):
    message = await ctx.send(f'Received command to add {url} to the queue.')

    if os.path.isfile("music/" + url[24:] + '.mp3'):
        await message.edit(content=f'Successfully added {url}.mp3 to the download queue.')
    else:
        await message.edit(content=f'Starting download of {url}...')
        process = download(url, 'music/' + url[24:])
        percent = 0
        while process.poll() is None:
            await asyncio.sleep(1)
            new_percent = get_download_progress(url)
            if new_percent > percent:
                percent = new_percent
                await message.edit(content=f'Download progress: {percent}%')
        await message.edit(content=f'{url} has been downloaded.')

    with open('queue.json', 'r') as f:
        data = json.load(f)
    voice_channel_id = str(ctx.author.voice.channel.id)
    file_name = url[24:] + '.mp3'
    if voice_channel_id in data:
        data[voice_channel_id].append(file_name)
    else:
        data[voice_channel_id] = [file_name]
    with open('queue.json', 'w') as f:
        json.dump(data, f, indent=4)




def download(url, destination):
    cmd = f'yt-dlp -x -o "{destination}.mp3" --audio-format mp3 {url}'
    process = subprocess.Popen(cmd, shell=True)
    return process

def get_download_progress(url):
        return 0
