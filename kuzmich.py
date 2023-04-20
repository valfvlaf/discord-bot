from easy_voice import object
from discord.ext import commands

Kuzmich = object.Kuzmich()

@Kuzmich.bot.command()
async def play(ctx):
    await Kuzmich.play(ctx)

@Kuzmich.bot.command()
async def add(ctx, url):
    await Kuzmich.add(ctx, url)

@Kuzmich.bot.command()
async def queue(ctx):
    await Kuzmich.queue(ctx)

@Kuzmich.bot.command()
async def skip(ctx):
    await Kuzmich.skip(ctx)

@Kuzmich.bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда не найдена. Используйте !help, чтобы узнать доступные команды.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Недостаточно аргументов для выполнения команды. Проверьте правильность ввода команды.")
    else:
        await ctx.send(f"Произошла ошибка: {error}")

Kuzmich.bot.run('MTA5NjQ0NDQ4NjYyNTgwNDM4OA.GH5Igv.Ts7mGGfP3QmZl_6YSqF41gGmf4Rjw-6rLsf5go')