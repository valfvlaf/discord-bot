import os

MY_USER_ID = 339638167697096706

async def clear_bot_data(self,   ctx):
    # Получаем ID пользователя, который вызвал команду
    user_id = ctx.message.author.id

    # Проверяем, совпадает ли ID пользователя с вашим ID
    if user_id == MY_USER_ID:
        # Если совпадает, удаляем все файлы из папки music
        for filename in os.listdir("music"):
            os.remove(os.path.join("music", filename))
        await ctx.send("Все файлы в папке music удалены")
    else:
        # Если не совпадает, отправляем сообщение "У вас нет прав выполнить эту функцию"
        await ctx.send("У вас нет прав выполнить эту функцию")