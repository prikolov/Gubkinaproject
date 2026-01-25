"""
Обработчик текстовых сообщений
"""

from aiogram import types

async def handle_text(message: types.Message):
    """Обработка текстовых сообщений"""
    try:
        text = message.text
        
        # Простое суммаризирование (базовый алгоритм)
        summary = summarize_text(text, style="standard")
        
        await message.answer(
            f"📝 **Исходный текст:**\n{text}\n\n"
            f"✨ **Резюме:**\n{summary}"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

def summarize_text(text: str, style: str = "standard") -> str:
    """Простое суммаризирование текста"""
    sentences = text.split(". ")
    
    if style == "short":
        # Очень коротко - первое предложение
        return sentences[0] + "."
    elif style == "bullets":
        # Ключевые пункты - первые 3 предложения
        return " ".join(s + "." for s in sentences[:3])
    elif style == "detailed":
        # Подробное - весь текст
        return text
    else:  # standard
        # Стандартное - первые 2 предложения
        return " ".join(s + "." for s in sentences[:2])
