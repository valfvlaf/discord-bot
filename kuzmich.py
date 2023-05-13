from discord.ext import commands
from easy_voice import object

token = "MTA5ODY4NDc2MzcxMzMxNDk0OA.GWZkQY.G57b2s7bjowYgr2aeo9ZJiWI9M-9JFH3hwaqCc"

Kuzmich = object.Kuzmich()

@Kuzmich.bot.command()
async def k(ctx, command=None, *args):
    """
    This command allows users to interact with Kuzmich.
    Available logic: play, add, queue, skip.
    Usage: !kuzmich <command> <args>

    Parameters:
        command (str): The command to execute. Must be one of: play, add, queue, skip.
        args (list of str): The arguments to pass to the command.
    """
    commands = {
        'play': Kuzmich.play,
        'add': Kuzmich.add,
        'queue': Kuzmich.queue,
        'skip': Kuzmich.skip,
        'clear_bot_data': Kuzmich.clear_bot_data
    }
    if command not in commands:
        await ctx.send('Invalid command.')
        return
    await commands[command](ctx, *args)

@Kuzmich.bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда не найдена. Используйте .help, чтобы узнать доступные команды.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Недостаточно аргументов для выполнения команды. Проверьте правильность ввода команды.")
    else:
        await ctx.send(f"Произошла ошибка: {error}")

Kuzmich.bot.run(token)