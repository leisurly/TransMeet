"""語音轉文字服務類別。

此模組提供使用 Whisper 模型進行語音辨識的功能。
主要類別 TranscriptionService 負責載入 Whisper 模型、
執行語音轉文字、格式化結果和生成字幕等功能。

Typical usage example:
    service = TranscriptionService()
    result = service.transcribe_audio("audio.wav", language="zh")
    if result["success"]:
        text = result["transcription"]["full_text"]
"""

import torch
import whisper
from typing import Dict, List, Optional, Any
from datetime import datetime

from config.settings import Config
from utils.file_utils import FileUtils


class TranscriptionService:
    """語音轉文字服務類別。
    
    負責使用 Whisper 模型進行語音辨識，提供完整的語音轉文字功能，
    包括模型載入、轉錄執行、結果格式化和字幕生成等。
    
    Attributes:
        config: 配置設定物件
        device: 計算裝置 (CPU/GPU)
        model: Whisper 模型實例
        file_utils: 檔案工具類別
    """
    
    def __init__(self) -> None:
        """初始化轉錄服務。
        
        設定配置、計算裝置和檔案工具類別。
        """
        self.config = Config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.file_utils = FileUtils()
    
    def load_model(self, model_name: Optional[str] = None) -> bool:
        """載入 Whisper 模型。
        
        載入指定的 Whisper 模型到記憶體中，支援 GPU 加速。
        
        Args:
            model_name: 模型名稱，預設使用配置中的模型
            
        Returns:
            是否載入成功
            
        Raises:
            Exception: 當模型載入失敗時
        """
        try:
            if model_name is None:
                model_name = self.config.WHISPER_SETTINGS["model_name"]
            
            self.model = whisper.load_model(model_name, device=self.device)
            return True
        except Exception as e:
            print(f"載入模型失敗: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """轉錄音訊檔案。
        
        使用 Whisper 模型對音訊檔案進行語音轉文字處理，
        支援多語言和時間戳記功能。
        
        Args:
            audio_path: 音訊檔案路徑
            language: 語言代碼，預設使用配置中的語言
            
        Returns:
            包含轉錄結果的字典，成功時包含轉錄文字和相關資訊，
            失敗時包含錯誤訊息。
            
        Raises:
            RuntimeError: 當無法載入 Whisper 模型時
        """
        try:
            if self.model is None:
                if not self.load_model():
                    raise RuntimeError("無法載入 Whisper 模型")
            
            if language is None:
                language = self.config.WHISPER_SETTINGS["language"]
            
            # 執行轉錄
            result = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True,
                verbose=False
            )
            
            # 格式化結果
            formatted_result = self._format_transcription_result(result, audio_path)
            
            return {
                "success": True,
                "transcription": formatted_result,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def transcribe_with_timestamps(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """轉錄音訊並包含詳細時間戳記。
        
        執行語音轉文字並生成包含單詞級時間戳記的詳細結果，
        適用於字幕生成和精確時間定位。
        
        Args:
            audio_path: 音訊檔案路徑
            language: 語言代碼
            
        Returns:
            包含詳細時間戳記的轉錄結果字典
        """
        try:
            if self.model is None:
                if not self.load_model():
                    raise RuntimeError("無法載入 Whisper 模型")
            
            if language is None:
                language = self.config.WHISPER_SETTINGS["language"]
            
            # 執行轉錄
            result = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True,
                verbose=False
            )
            
            # 格式化時間戳記結果
            formatted_result = self._format_timestamp_result(result, audio_path)
            
            return {
                "success": True,
                "transcription": formatted_result,
                "language": language,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _format_transcription_result(self, result: Dict, audio_path: str) -> Dict[str, Any]:
        """格式化轉錄結果。
        
        將 Whisper 的原始轉錄結果格式化為標準格式，
        包含完整文字、段落資訊和置信度等。
        
        Args:
            result: Whisper 轉錄結果
            audio_path: 音訊檔案路徑
            
        Returns:
            格式化後的結果字典
        """
        return {
            "full_text": result["text"].strip(),
            "segments": [
                {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip(),
                    "confidence": segment.get("avg_logprob", 0.0)
                }
                for segment in result["segments"]
            ],
            "language": result.get("language", "unknown"),
            "audio_path": audio_path
        }
    
    def _format_timestamp_result(self, result: Dict, audio_path: str) -> Dict[str, Any]:
        """格式化時間戳記結果。
        
        將 Whisper 的轉錄結果格式化為包含單詞級時間戳記的詳細格式，
        適用於字幕生成和精確時間定位。
        
        Args:
            result: Whisper 轉錄結果
            audio_path: 音訊檔案路徑
            
        Returns:
            格式化後的時間戳記結果字典
        """
        segments = []
        
        for segment in result["segments"]:
            segment_data = {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "confidence": segment.get("avg_logprob", 0.0),
                "words": []
            }
            
            # 處理單詞級時間戳記
            if "words" in segment:
                for word in segment["words"]:
                    segment_data["words"].append({
                        "word": word["word"],
                        "start": word["start"],
                        "end": word["end"],
                        "confidence": word.get("probability", 0.0)
                    })
            
            segments.append(segment_data)
        
        return {
            "full_text": result["text"].strip(),
            "segments": segments,
            "language": result.get("language", "unknown"),
            "audio_path": audio_path
        }
    
    def save_transcription(self, transcription: Dict, output_path: str) -> bool:
        """
        儲存轉錄結果
        
        Args:
            transcription: 轉錄結果
            output_path: 輸出檔案路徑
            
        Returns:
            是否儲存成功
        """
        return self.file_utils.save_json(transcription, output_path)
    
    def generate_subtitles(self, transcription: Dict, format_type: str = "srt") -> str:
        """
        生成字幕檔案
        
        Args:
            transcription: 轉錄結果
            format_type: 字幕格式 (srt, vtt)
            
        Returns:
            字幕內容
        """
        if format_type.lower() == "srt":
            return self._generate_srt_subtitles(transcription)
        elif format_type.lower() == "vtt":
            return self._generate_vtt_subtitles(transcription)
        else:
            raise ValueError(f"不支援的字幕格式: {format_type}")
    
    def _generate_srt_subtitles(self, transcription: Dict) -> str:
        """生成 SRT 格式字幕"""
        srt_content = []
        
        for i, segment in enumerate(transcription["segments"], 1):
            start_time = self._format_time_srt(segment["start"])
            end_time = self._format_time_srt(segment["end"])
            text = segment["text"]
            
            srt_content.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
        
        return "\n".join(srt_content)
    
    def _generate_vtt_subtitles(self, transcription: Dict) -> str:
        """生成 VTT 格式字幕"""
        vtt_content = ["WEBVTT\n"]
        
        for segment in transcription["segments"]:
            start_time = self._format_time_vtt(segment["start"])
            end_time = self._format_time_vtt(segment["end"])
            text = segment["text"]
            
            vtt_content.append(f"{start_time} --> {end_time}\n{text}\n")
        
        return "\n".join(vtt_content)
    
    def _format_time_srt(self, seconds: float) -> str:
        """格式化 SRT 時間格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _format_time_vtt(self, seconds: float) -> str:
        """格式化 VTT 時間格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}" 