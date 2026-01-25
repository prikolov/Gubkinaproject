"""
Конфигурация бота
"""

import os
from dotenv import load_dotenv

# Загрузи переменные окружения
load_dotenv()

# Получи токен
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка
if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не найден в .env файле!")

print(f"✅ Токен загружен: {BOT_TOKEN[:10]}...")
