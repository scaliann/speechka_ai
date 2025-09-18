from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, MenuButtonDefault


async def setup_menu(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="🏠 Главное меню"),
            BotCommand(command="help", description="❓ Помощь 📖"),
            BotCommand(
                command="agreement", description="🏛️ Пользовательское соглашение"
            ),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
    await bot.set_chat_menu_button(menu_button=MenuButtonDefault())
