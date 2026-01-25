"""
Обработчик команд меню
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboard_builder import build_settings_keyboard

async def handle_start(message: types.Message):
    """Команда /start"""
    await message.answer(
        "👋 Привет! Я Telegram Audio Bot.\n\n"
        "Я могу:\n"
        "🗣️ Транскрибировать голосовые сообщения\n"
        "📝 Суммаризировать текст\n\n"
        "Просто отправь мне голосовое сообщение или текст!",
        reply_markup=build_settings_keyboard()
    )

async def handle_help(message: types.Message):
    """Команда /help"""
    await message.answer(
        "📖 **Справка:**\n\n"
        "/start - Начать\n"
        "/help - Эта справка\n"
        "/settings - Настройки языка и стиля\n"
        "/cancel - Отменить текущую операцию\n\n"
        "**Как использовать:**\n"
        "1️⃣ Отправь голосовое сообщение или текст\n"
        "2️⃣ Выбери язык и стиль через /settings\n"
        "3️⃣ Получи результат!"
    )

async def handle_settings(message: types.Message, state: FSMContext):
    """Команда /settings"""
    await message.answer(
        "⚙️ **Настройки:**",
        reply_markup=build_settings_keyboard()
    )

async def handle_cancel(message: types.Message, state: FSMContext):
    """Команда /cancel"""
    await state.clear()
    await message.answer("❌ Операция отменена.")
