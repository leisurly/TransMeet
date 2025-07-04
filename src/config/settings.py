"""
系統配置設定
包含所有應用程式的配置參數
"""

import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """系統配置類別"""
    
    # 基礎路徑設定
    BASE_DIR = Path(__file__).parent.parent.parent
    UPLOADS_DIR = BASE_DIR / "uploads"
    RESULTS_DIR = BASE_DIR / "results"
    MODELS_DIR = BASE_DIR / "models"
    
    # 音訊處理設定
    AUDIO_SETTINGS = {
        "sample_rate": 16000,
        "chunk_duration": 30,  # 秒
        "supported_formats": [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
    }
    
    # Whisper 模型設定
    WHISPER_SETTINGS = {
        "model_name": "openai/whisper-base",
        "language": "zh",
        "task": "transcribe"
    }
    
    # LLM 設定
    LLM_SETTINGS = {
        "provider": "openai",  # 或 "local"
        "model": "gpt-3.5-turbo",
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    # 說話者識別設定
    SPEAKER_SETTINGS = {
        "min_speakers": 1,
        "max_speakers": 10,
        "clustering_method": "spectral"
    }
    
    # Streamlit 設定
    STREAMLIT_SETTINGS = {
        "page_title": "會議記錄語音辨識系統",
        "page_icon": "🎤",
        "layout": "wide"
    }
    
    @classmethod
    def get_upload_path(cls) -> Path:
        """取得上傳檔案路徑"""
        cls.UPLOADS_DIR.mkdir(exist_ok=True)
        return cls.UPLOADS_DIR
    
    @classmethod
    def get_results_path(cls) -> Path:
        """取得結果檔案路徑"""
        cls.RESULTS_DIR.mkdir(exist_ok=True)
        return cls.RESULTS_DIR
    
    @classmethod
    def get_models_path(cls) -> Path:
        """取得模型檔案路徑"""
        cls.MODELS_DIR.mkdir(exist_ok=True)
        return cls.MODELS_DIR
    
    @classmethod
    def get_llm_api_key(cls) -> str:
        """取得 LLM API 金鑰"""
        return os.getenv("OPENAI_API_KEY", "")
    
    @classmethod
    def validate_audio_format(cls, filename: str) -> bool:
        """驗證音訊檔案格式"""
        return any(filename.lower().endswith(fmt) for fmt in cls.AUDIO_SETTINGS["supported_formats"]) 