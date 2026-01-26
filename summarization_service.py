import g4f
import asyncio
from config import SUMMARY_STYLES

# Отключаем логирование ошибок g4f, чтобы не мусорить в консоли
g4f.debug.logging = False

async def generate_summary(text: str, style_key: str) -> str:
    """
    Генерирует резюме с помощью бесплатного GPT-4o-mini (через g4f)
    """
    # 1. Получаем настройки стиля
    style_info = SUMMARY_STYLES.get(style_key, SUMMARY_STYLES["default"])
    system_prompt = style_info["prompt"]

    # 2. Формируем историю сообщений
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Сделай резюме этого текста:\n\n{text}"}
    ]

    try:
        # 3. Запрос к нейросети (пробуем разных провайдеров если один упадет)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4o_mini,
            messages=messages,
        )

        if response and isinstance(response, str) and len(response) > 10:
            return response.strip()

        # Если ответ пустой, пробуем запасной вариант (GPT-3.5)
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_35_turbo,
            messages=messages,
        )
        return response.strip() if response else "⚠️ Нейросеть вернула пустой ответ."

    except Exception as e:
        print(f"Ошибка LLM: {e}")
        # Фолбэк: если нейросеть недоступна, возвращаем начало текста
        return f"⚠️ Режим оффлайн (ошибка сети). Начало текста:\n{text[:500]}..."
