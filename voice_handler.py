"""
Обработчик голосовых сообщений с поддержкой стилей суммаризации
"""

import os
import subprocess
import asyncio
from aiogram import types, Bot
import whisper


async def handle_voice(message: types.Message, bot: Bot):
    """Обработка голосовых сообщений и аудиофайлов"""
    try:
        # Импортируем внутри функции, чтобы избежать циклического импорта
        from settings_handler import get_user_settings, apply_summarization_style

        status_msg = await message.answer("⏳ Загружаю модель Whisper...")

        # Скачивание файла
        file_info = await bot.get_file(message.voice.file_id)
        file_path = file_info.file_path

        # Сохранение аудиофайла
        audio_file = "audio_temp.ogg"
        await bot.download_file(file_path, audio_file)

        # Конвертирование в WAV если нужно
        wav_file = await convert_to_wav(audio_file)

        # Загрузка модели Whisper
        model = whisper.load_model("base")

        # Обновляем статус
        await status_msg.edit_text("🎤 Транскрибирую аудио...\n⏳ Это может занять несколько минут...")

        # Получаем настройки пользователя
        user_settings = get_user_settings(message.from_user.id)
        language = user_settings.get("language", "ru")
        style = user_settings.get("style", "standard")

        # Транскрибирование в отдельном потоке (не блокирует бота)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: model.transcribe(wav_file, language=language))
        text = result["text"]

        # Применяем выбранный стиль
        processed_text = apply_summarization_style(text, style)

        # Отправка результата (разбиваем если слишком длинный)
        await send_long_message(bot, message.chat.id, f"📝 **Транскрипция:**\n\n{processed_text}", status_msg)

        # Очистка временных файлов
        cleanup_files([audio_file, wav_file])

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

async def handle_audio_file(message: types.Message, bot: Bot):
    """Обработка загруженных аудиофайлов (MP3, WAV и т.д.)"""
    try:
        # Импортируем внутри функции, чтобы избежать циклического импорта
        from settings_handler import get_user_settings, apply_summarization_style

        status_msg = await message.answer("⏳ Загружаю модель Whisper...")

        # Определяем тип файла
        if message.audio:
            file_info = await bot.get_file(message.audio.file_id)
            filename = message.audio.file_name or "audio_file.mp3"
        elif message.document:
            file_info = await bot.get_file(message.document.file_id)
            filename = message.document.file_name or "audio_file"
        else:
            await message.answer("❌ Неподдерживаемый тип файла")
            return

        # Скачиваем файл
        file_path = file_info.file_path
        await bot.download_file(file_path, filename)

        # Конвертируем в WAV
        wav_file = await convert_to_wav(filename)

        # Загрузка модели
        model = whisper.load_model("base")

        # Обновляем статус
        await status_msg.edit_text("🎤 Транскрибирую аудио...\n⏳ Это может занять несколько минут...")

        # Получаем настройки пользователя
        user_settings = get_user_settings(message.from_user.id)
        language = user_settings.get("language", "ru")
        style = user_settings.get("style", "standard")

        # Транскрибирование в отдельном потоке
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: model.transcribe(wav_file, language=language))
        text = result["text"]

        # Применяем выбранный стиль
        processed_text = apply_summarization_style(text, style)

        # Отправка результата (разбиваем если слишком длинный)
        await send_long_message(bot, message.chat.id, f"📝 **Транскрипция:**\n\n{processed_text}", status_msg)

        # Очистка
        cleanup_files([filename, wav_file])

    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

async def send_long_message(bot: Bot, chat_id: int, text: str, original_msg: types.Message = None, max_length: int = 4000):
    """Отправляет длинный текст, разбивая его на части если необходимо"""

    if len(text) <= max_length:
        # Если текст короткий, просто обновляем исходное сообщение
        if original_msg:
            await original_msg.edit_text(text)
        else:
            await bot.send_message(chat_id, text)
        return

    # Если текст длинный, разбиваем его
    # Сначала обновляем исходное сообщение с первой частью
    first_part = text[:max_length]
    if original_msg:
        await original_msg.edit_text(first_part)
    else:
        await bot.send_message(chat_id, first_part)

    # Остаток текста отправляем отдельными сообщениями
    remaining_text = text[max_length:]

    while remaining_text:
        # Отправляем следующие 4000 символов
        part = remaining_text[:max_length]
        await bot.send_message(chat_id, part)
        remaining_text = remaining_text[max_length:]

async def convert_to_wav(input_file: str) -> str:
    """Конвертирование аудиофайла в WAV формат"""
    wav_file = "audio_temp.wav"

    try:
        # Используем FFmpeg для конвертирования
        subprocess.run(
            ["ffmpeg", "-i", input_file, "-acodec", "pcm_s16le", "-ar", "16000", wav_file, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return wav_file
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Если FFmpeg не установлен, используем исходный файл
        return input_file

def cleanup_files(files: list):
    """Удаление временных файлов"""
    for file in files:
        if file and os.path.exists(file):
            try:
                os.remove(file)
            except:
                pass