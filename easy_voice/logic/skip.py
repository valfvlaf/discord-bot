from discord.utils import get

async def skip(kuzmich, ctx):
    voice_client = get(kuzmich.bot.voice_clients, guild=ctx.guild)

    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Song skipped.')
    else:
        await ctx.send('No playback to stop.')
