import json

async def queue(self, ctx):
    await ctx.message.delete()
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
