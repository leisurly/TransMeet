"""
音訊處理工具類別
提供音訊檔案處理相關的實用功能
"""

import librosa
import soundfile as sf
import numpy as np
from typing import Tuple, Optional, Dict, Any
from pathlib import Path


class AudioUtils:
    """音訊處理工具類別"""
    
    @staticmethod
    def load_audio(filepath: str, target_sr: int = 16000) -> Tuple[np.ndarray, int]:
        """
        載入音訊檔案並重採樣
        
        Args:
            filepath: 音訊檔案路徑
            target_sr: 目標採樣率
            
        Returns:
            (音訊資料, 採樣率)
        """
        try:
            audio, sr = librosa.load(filepath, sr=target_sr)
            return audio, sr
        except Exception as e:
            raise ValueError(f"載入音訊檔案失敗: {e}")
    
    @staticmethod
    def save_audio(audio: np.ndarray, filepath: str, sr: int = 16000) -> bool:
        """
        儲存音訊檔案
        
        Args:
            audio: 音訊資料
            filepath: 儲存路徑
            sr: 採樣率
            
        Returns:
            是否儲存成功
        """
        try:
            sf.write(filepath, audio, sr)
            return True
        except Exception as e:
            print(f"儲存音訊檔案失敗: {e}")
            return False
    
    @staticmethod
    def get_audio_info(filepath: str) -> Dict[str, Any]:
        """
        取得音訊檔案資訊
        
        Args:
            filepath: 音訊檔案路徑
            
        Returns:
            音訊資訊字典
        """
        try:
            # 取得基本資訊
            info = sf.info(filepath)
            
            # 載入音訊以取得更多資訊
            audio, sr = librosa.load(filepath, sr=None)
            
            return {
                "duration": len(audio) / sr,
                "sample_rate": sr,
                "channels": info.channels,
                "format": info.format,
                "subtype": info.subtype,
                "frames": len(audio),
                "file_size": Path(filepath).stat().st_size
            }
        except Exception as e:
            raise ValueError(f"取得音訊資訊失敗: {e}")
    
    @staticmethod
    def normalize_audio(audio: np.ndarray) -> np.ndarray:
        """
        正規化音訊
        
        Args:
            audio: 音訊資料
            
        Returns:
            正規化後的音訊資料
        """
        if len(audio) == 0:
            return audio
        
        # 計算 RMS
        rms = np.sqrt(np.mean(audio**2))
        if rms > 0:
            # 正規化到 -20 dB
            target_rms = 10**(-20/20)
            audio = audio * (target_rms / rms)
        
        return audio
    
    @staticmethod
    def trim_silence(audio: np.ndarray, threshold_db: float = -40) -> np.ndarray:
        """
        移除靜音部分
        
        Args:
            audio: 音訊資料
            threshold_db: 靜音閾值 (dB)
            
        Returns:
            處理後的音訊資料
        """
        threshold = 10**(threshold_db/20)
        return librosa.effects.trim(audio, top_db=abs(threshold_db))[0]
    
    @staticmethod
    def split_audio(audio: np.ndarray, sr: int, chunk_duration: float = 30) -> list:
        """
        分割音訊為多個片段
        
        Args:
            audio: 音訊資料
            sr: 採樣率
            chunk_duration: 每個片段的時長（秒）
            
        Returns:
            音訊片段列表
        """
        chunk_samples = int(chunk_duration * sr)
        chunks = []
        
        for i in range(0, len(audio), chunk_samples):
            chunk = audio[i:i + chunk_samples]
            if len(chunk) > 0:
                chunks.append(chunk)
        
        return chunks
    
    @staticmethod
    def detect_speech_segments(audio: np.ndarray, sr: int, 
                             min_silence_duration: float = 0.5) -> list:
        """
        檢測語音段落
        
        Args:
            audio: 音訊資料
            sr: 採樣率
            min_silence_duration: 最小靜音時長（秒）
            
        Returns:
            語音段落列表 [(start_time, end_time), ...]
        """
        # 使用 librosa 的語音活動檢測
        intervals = librosa.effects.split(
            audio, 
            top_db=20, 
            frame_length=2048, 
            hop_length=512
        )
        
        segments = []
        for start, end in intervals:
            start_time = start / sr
            end_time = end / sr
            
            # 過濾太短的段落
            if end_time - start_time >= min_silence_duration:
                segments.append((start_time, end_time))
        
        return segments
    
    @staticmethod
    def calculate_spectral_features(audio: np.ndarray, sr: int) -> Dict[str, float]:
        """
        計算頻譜特徵
        
        Args:
            audio: 音訊資料
            sr: 採樣率
            
        Returns:
            頻譜特徵字典
        """
        # 計算梅爾頻譜圖
        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr)
        
        # 計算各種特徵
        features = {
            "spectral_centroid": float(np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))),
            "spectral_bandwidth": float(np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=sr))),
            "spectral_rolloff": float(np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))),
            "zero_crossing_rate": float(np.mean(librosa.feature.zero_crossing_rate(audio))),
            "mfcc_mean": float(np.mean(librosa.feature.mfcc(y=audio, sr=sr))),
            "rms_energy": float(np.sqrt(np.mean(audio**2)))
        }
        
        return features 