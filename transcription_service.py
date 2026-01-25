"""
Сервис транскрибации с использованием OpenAI Whisper
Конвертирование аудиоформатов и распознавание речи
"""

import os
import subprocess
import torch
from pathlib import Path

try:
    import whisper
except ImportError:
    whisper = None

class TranscriptionService:
    """Сервис для транскрибации аудио"""
    
    def __init__(self, model_name="medium"):
        self.model_name = model_name
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_model(self):
        """Загрузка модели Whisper"""
        if whisper is None:
            raise ImportError("whisper not installed. Run: pip install openai-whisper")
        self.model = whisper.load_model(self.model_name, device=self.device)
    
    async def transcribe(self, audio_path: str, language: str = "auto") -> str:
        """Транскрибация аудиофайла"""
        if self.model is None:
            self.load_model()
        
        audio = whisper.load_audio(audio_path)
        result = self.model.transcribe(
            audio, 
            language=None if language == "auto" else language
        )
        return result["text"]
    
    async def convert_to_wav(self, input_path: str, output_path: str):
        """Конвертирование аудио в WAV формат через FFmpeg"""
        cmd = [
            "ffmpeg", "-i", input_path,
            "-acodec", "pcm_s16le", "-ar", "16000",
            output_path, "-y"
        ]
        subprocess.run(cmd, capture_output=True)
