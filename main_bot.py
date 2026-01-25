"""
Главный файл Telegram бота для обработки аудио и текста
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN
from menu_handler import handle_start, handle_help, handle_settings, handle_cancel
from voice_handler import handle_voice, handle_audio_file
from text_handler import handle_text
from settings_handler import SettingsState, handle_language_callback, handle_style_callback
from menu_setup import setup_menu
from keyboard_builder import build_settings_keyboard

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==================== РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ ====================

# Команды
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await handle_start(message)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await handle_help(message)

@dp.message(Command("settings"))
async def settings_command(message: types.Message, state: FSMContext):
    await handle_settings(message, state)

@dp.message(Command("cancel"))
async def cancel_command(message: types.Message, state: FSMContext):
    await handle_cancel(message, state)

# Голосовые сообщения
@dp.message(F.voice)
async def voice_message(message: types.Message):
    await handle_voice(message, bot)

# Аудиофайлы (MP3, WAV и т.д.)
@dp.message(F.audio)
async def audio_message(message: types.Message):
    await handle_audio_file(message, bot)

# Документы (если отправлены как файлы)
@dp.message(F.document)
async def document_message(message: types.Message):
    if message.document.mime_type and "audio" in message.document.mime_type:
        await handle_audio_file(message, bot)
    else:
        await message.answer("❌ Это не аудиофайл. Отправь MP3, WAV или голосовое сообщение!")

# Текстовые сообщения (когда не в состоянии выбора)
@dp.message(StateFilter(None), F.text)
async def text_message(message: types.Message):
    await handle_text(message)

# Выбор языка (callback)
@dp.callback_query(F.data.startswith("lang_"))
async def language_callback(callback: types.CallbackQuery, state: FSMContext):
    await handle_language_callback(callback, state)

# Выбор стиля (callback)
@dp.callback_query(F.data.startswith("style_"))
async def style_callback(callback: types.CallbackQuery, state: FSMContext):
    await handle_style_callback(callback, state)

# Открыть меню настроек
@dp.callback_query(F.data == "set_language")
async def set_language_callback(callback: types.CallbackQuery):
    from keyboard_builder import build_language_keyboard
    await callback.message.edit_text(
        "🗣️ Выбери язык транскрибации:",
        reply_markup=build_language_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "set_style")
async def set_style_callback(callback: types.CallbackQuery):
    from keyboard_builder import build_style_keyboard
    await callback.message.edit_text(
        "💡 Выбери стиль резюме:",
        reply_markup=build_style_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "close")
async def close_callback(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

async def main():
    """Запуск бота"""
    logger.info("Bot started")

    # Настройка меню команд
    await setup_menu(bot)

    # Запуск polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())