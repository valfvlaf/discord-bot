import discord
from discord.ext import commands
from easy_voice.logic.play import play
from easy_voice.logic.add import add
from easy_voice.logic.queue import queue
from easy_voice.logic.skip import skip
from easy_voice.logic.clear_bot_data import clear_bot_data

class Kuzmich:
    def __init__(self):
        self.bot = commands.Bot(command_prefix='+', intents=discord.Intents.all())

    async def play(self, ctx):
        await play(self, ctx)

    async def add(self, ctx, url):
        await add(self, ctx, url)

    async def queue(self, ctx):
        await queue(self, ctx)

    async def skip(self, ctx):
        await skip(self, ctx)

    async def clear_bot_data(self, ctx):
        await clear_bot_data(self, ctx)
