"""
Настройка меню команд Telegram
"""

from aiogram import Bot
from aiogram.types import BotCommand

async def setup_menu(bot: Bot):
    """Регистрация команд в меню"""
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="help", description="Справка"),
        BotCommand(command="settings", description="Настройки"),
        BotCommand(command="cancel", description="Отмена"),
    ]
    
    await bot.set_my_commands(commands)
