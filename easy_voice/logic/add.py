import os
import json
import subprocess
import logging
import re

logging.basicConfig(filename='output.log', level=logging.DEBUG)

async def add(self, ctx, url):
    await ctx.message.delete()
    message = await ctx.send(f'Received command to add {get_video_title(url)} to the queue.')
    if os.path.isfile("music/" + url[24:] + '.mp3'):
        await message.edit(content=f'Successfully added {get_video_title(url)}.mp3 to the download queue.')
    else:
        await message.edit(content=f'Starting download of {get_video_title(url)}...')
        await download(url, 'music/' + get_video_title(url), message)
        await message.edit(content=f'{get_video_title(url)} has been downloaded.')

    with open('queue.json', 'r') as f:
        data = json.load(f)
    voice_channel_id = str(ctx.author.voice.channel.id)
    file_name = get_video_title(url) + '.mp3'
    if voice_channel_id in data:
        data[voice_channel_id].append(file_name)
    else:
        data[voice_channel_id] = [file_name]
    with open('queue.json', 'w') as f:
        json.dump(data, f, indent=4)

def get_video_title(url):
    cmd = f'yt-dlp --dump-json {url}'
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    info = json.loads(output)
    return info['title']

async def download(url, destination, message):
    cmd = f'yt-dlp -x -o "{destination}.mp3" --audio-format mp3 {url}'
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True) as process:
        with open("output.log", "w") as log:#проклято
            for line in process.stdout:
                log.write(line)
                match = re.search(r'(\d+(\.\d+)?)%', line)#да простит меня Аллах
                if match:
                    await message.edit(content=f'Download progress: {match.group(1)}%')
    return process
