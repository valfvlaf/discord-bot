import subprocess
import logging
import re

logging.basicConfig(filename='output.log', level=logging.DEBUG)

url = 'https://www.youtube.com/watch?v=Rj0R-S4KH6Y'
destination = 'music/' + 'rickroll'
cmd = f'yt-dlp -v -x -o "{destination}.mp3" --audio-format mp3 {url}'

with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
    with open("output.log", "w") as log:
        for line in process.stdout:
            log.write(line)
            match = re.search(r'(\d+(\.\d+)?)%', line)
            if match:
                print(match.group(1), end="\n")

