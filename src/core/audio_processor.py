"""
音訊處理核心類別
負責音訊檔案的載入、預處理和基本分析
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from config.settings import Config
from utils.audio_utils import AudioUtils


class AudioProcessor:
    """音訊處理核心類別"""
    
    def __init__(self):
        """初始化音訊處理器"""
        self.config = Config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.audio_utils = AudioUtils()
    
    def process_audio_file(self, filepath: str) -> Dict[str, Any]:
        """
        處理音訊檔案
        
        Args:
            filepath: 音訊檔案路徑
            
        Returns:
            處理結果字典
        """
        try:
            # 驗證檔案格式
            if not self.config.validate_audio_format(filepath):
                raise ValueError(f"不支援的音訊格式: {Path(filepath).suffix}")
            
            # 取得檔案資訊
            file_info = self.audio_utils.get_audio_info(filepath)
            
            # 載入音訊
            audio, sr = self.audio_utils.load_audio(
                filepath, 
                target_sr=self.config.AUDIO_SETTINGS["sample_rate"]
            )
            
            # 預處理音訊
            processed_audio = self._preprocess_audio(audio)
            
            # 檢測語音段落
            speech_segments = self.audio_utils.detect_speech_segments(
                processed_audio, 
                sr
            )
            
            # 計算頻譜特徵
            spectral_features = self.audio_utils.calculate_spectral_features(
                processed_audio, 
                sr
            )
            
            return {
                "success": True,
                "file_info": file_info,
                "audio_data": processed_audio,
                "sample_rate": sr,
                "speech_segments": speech_segments,
                "spectral_features": spectral_features,
                "duration": len(processed_audio) / sr
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _preprocess_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        預處理音訊
        
        Args:
            audio: 原始音訊資料
            
        Returns:
            預處理後的音訊資料
        """
        # 正規化
        audio = self.audio_utils.normalize_audio(audio)
        
        # 移除靜音
        audio = self.audio_utils.trim_silence(audio)
        
        return audio
    
    def split_audio_for_processing(self, audio: np.ndarray, sr: int) -> List[np.ndarray]:
        """
        將音訊分割為適合處理的片段
        
        Args:
            audio: 音訊資料
            sr: 採樣率
            
        Returns:
            音訊片段列表
        """
        chunk_duration = self.config.AUDIO_SETTINGS["chunk_duration"]
        return self.audio_utils.split_audio(audio, sr, chunk_duration)
    
    def get_audio_statistics(self, audio: np.ndarray, sr: int) -> Dict[str, Any]:
        """
        取得音訊統計資訊
        
        Args:
            audio: 音訊資料
            sr: 採樣率
            
        Returns:
            統計資訊字典
        """
        duration = len(audio) / sr
        
        return {
            "duration_seconds": duration,
            "duration_minutes": duration / 60,
            "total_samples": len(audio),
            "sample_rate": sr,
            "max_amplitude": float(np.max(np.abs(audio))),
            "mean_amplitude": float(np.mean(np.abs(audio))),
            "rms_energy": float(np.sqrt(np.mean(audio**2)))
        } 