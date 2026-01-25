"""
Построитель клавиатур и кнопок
Интерактивные элементы интерфейса Telegram
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def build_settings_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для меню настроек"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗣️ Выбрать язык", callback_data="set_language")],
        [InlineKeyboardButton(text="💡 Выбрать стиль резюме", callback_data="set_style")],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close")]
    ])
    return keyboard

def build_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора языка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Автоматический", callback_data="lang_auto")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr")],
        [InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es")],
    ])
    return keyboard

def build_style_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора стиля суммаризации"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Стандартное", callback_data="style_standard")],
        [InlineKeyboardButton(text="🤏 Очень коротко", callback_data="style_short")],
        [InlineKeyboardButton(text="🔑 Ключевые пункты", callback_data="style_bullets")],
        [InlineKeyboardButton(text="🧐 Подробное", callback_data="style_detailed")]
    ])
    return keyboard

def register_menu_handlers(dp):
    """Регистрация обработчиков меню (заглушка)"""
    pass
