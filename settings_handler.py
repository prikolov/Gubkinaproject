"""
Обработчик настроек и состояний (FSM) с суммаризацией через extractive методы
"""

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from collections import Counter

# Словарь для хранения настроек пользователей
user_settings = {}


class SettingsState(StatesGroup):
    """Состояния для FSM"""
    choosing_language = State()
    choosing_style = State()


def get_user_settings(user_id: int) -> dict:
    """Получить настройки пользователя"""
    if user_id not in user_settings:
        user_settings[user_id] = {
            "language": "ru",
            "style": "standard"
        }
    return user_settings[user_id]


def set_user_language(user_id: int, language: str):
    """Установить язык пользователя"""
    settings = get_user_settings(user_id)
    settings["language"] = language


def set_user_style(user_id: int, style: str):
    """Установить стиль суммаризации пользователя"""
    settings = get_user_settings(user_id)
    settings["style"] = style


async def handle_language_callback(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора языка"""
    language_map = {
        "lang_auto": ("auto", "🌍 Автоматический"),
        "lang_ru": ("ru", "🇷🇺 Русский"),
        "lang_en": ("en", "🇺🇸 English"),
        "lang_de": ("de", "🇩🇪 Deutsch"),
        "lang_fr": ("fr", "🇫🇷 Français"),
        "lang_es": ("es", "🇪🇸 Español"),
    }

    lang_code, lang_name = language_map.get(callback.data, ("ru", "Неизвестно"))

    # Сохраняем выбор пользователя
    set_user_language(callback.from_user.id, lang_code)

    await callback.message.edit_text(f"✅ Выбран язык: {lang_name}")
    await callback.answer(f"Язык установлен: {lang_name}")
    await state.clear()


async def handle_style_callback(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора стиля"""
    style_map = {
        "style_standard": ("standard", "📝 Стандартное"),
        "style_short": ("short", "🤏 Очень коротко"),
        "style_bullets": ("bullets", "🔑 Ключевые пункты"),
        "style_detailed": ("detailed", "🧐 Подробное"),
    }

    style_code, style_name = style_map.get(callback.data, ("standard", "Неизвестно"))

    # Сохраняем выбор пользователя
    set_user_style(callback.from_user.id, style_code)

    await callback.message.edit_text(f"✅ Выбран стиль: {style_name}")
    await callback.answer(f"Стиль установлен: {style_name}")
    await state.clear()


def apply_summarization_style(text: str, style: str) -> str:
    """Применить стиль суммаризации к тексту через TF-IDF алгоритм"""

    # Русские стоп-слова
    STOP_WORDS = {
        'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'а', 'то', 'все', 'она',
        'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только',
        'ее', 'мне', 'было', 'вот', 'от', 'ему', 'еще', 'нет', 'из', 'ему', 'теперь', 'даже',
        'ни', 'быть', 'ь', 'себя', 'ничего', 'ей', 'может', 'они', 'тем', 'чем', 'себе',
        'без', 'будто', 'человек', 'чего', 'раз', 'тоже', 'себя', 'под', 'жизнь', 'будто',
        'еще', 'ней', 'про', 'нибудь', 'какая', 'много', 'разве', 'три', 'эти', 'нас',
        'про', 'всех', 'них', 'какая', 'много', 'разве', 'три', 'эти', 'нас', 'про',
        'всех', 'них', 'какая', 'кто', 'этот', 'того', 'потом', 'себя', 'ничего', 'ей'
    }

    try:
        # Разбиваем на предложения
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 2:
            return text

        # Расчет TF-IDF для каждого предложения
        words_in_sentences = []
        all_words = []

        for sentence in sentences:
            # Преобразуем в нижний регистр и разбиваем на слова
            words = re.findall(r'\b\w+\b', sentence.lower())
            # Удаляем стоп-слова
            words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
            words_in_sentences.append(words)
            all_words.extend(words)

        # Считаем частотность слов
        word_freq = Counter(all_words)

        # Оцениваем предложения
        sentence_scores = {}
        for idx, words in enumerate(words_in_sentences):
            score = 0
            for word in words:
                score += word_freq[word]
            sentence_scores[idx] = score if words else 0

        # Определяем количество предложений для сохранения
        if style == "short":
            # 25% от исходного
            sentences_to_keep = max(1, len(sentences) // 4)

        elif style == "bullets":
            # 40% от исходного
            sentences_to_keep = max(2, int(len(sentences) * 0.4))

        elif style == "detailed":
            # Весь текст
            return text

        else:  # standard
            # 50% от исходного
            sentences_to_keep = max(2, len(sentences) // 2)

        # Выбираем лучшие предложения (в порядке появления)
        best_sentence_indices = sorted(
            sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:sentences_to_keep],
            key=lambda x: x[0]
        )

        # Собираем результат
        summary_sentences = [sentences[idx] for idx, _ in best_sentence_indices]
        result = '. '.join(summary_sentences)

        return result + '.' if result else text

    except Exception as e:
        # Fallback - если ошибка, возвращаем первые предложения
        print(f"Ошибка суммаризации: {e}")
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if style == "short":
            return sentences[0] + "." if sentences else text
        elif style == "bullets":
            return ". ".join(sentences[:3]) + "." if sentences else text
        else:
            return ". ".join(sentences[:2]) + "." if sentences else text