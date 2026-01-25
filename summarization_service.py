"""
Сервис суммаризации текста
Локальная обработка без внешних API
"""

class SummarizationService:
    """Сервис для суммаризации текста"""
    
    STYLES = {
        "standard": "standard",
        "short": "short",
        "bullets": "bullets",
        "detailed": "detailed"
    }
    
    @staticmethod
    async def summarize(text: str, style: str = "standard") -> str:
        """Суммаризация текста в выбранном стиле"""
        
        if style == "short":
            # Очень короткое резюме (1-2 предложения)
            sentences = text.split(".")
            result = ".".join(sentences[:2]).strip()
            if result and not result.endswith("."):
                result += "."
            return result
        
        elif style == "bullets":
            # Ключевые пункты
            sentences = text.split(".")
            bullets = [f"• {s.strip()}" for s in sentences[:4] if s.strip()]
            return "\n".join(bullets)
        
        elif style == "detailed":
            # Подробное (весь текст)
            return text
        
        else:  # standard (по умолчанию)
            # Стандартное резюме (2-3 предложения)
            sentences = text.split(".")
            result = ".".join(sentences[:3]).strip()
            if result and not result.endswith("."):
                result += "."
            return result
