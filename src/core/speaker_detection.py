"""
說話者識別類別
負責識別和區分不同的說話者
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from ..config.settings import Config
from ..utils.audio_utils import AudioUtils


class SpeakerDetection:
    """說話者識別類別"""
    
    def __init__(self):
        """初始化說話者識別器"""
        self.config = Config()
        self.audio_utils = AudioUtils()
    
    def detect_speakers(self, audio_data: np.ndarray, sr: int) -> Dict[str, Any]:
        """
        檢測說話者
        
        Args:
            audio_data: 音訊資料
            sr: 採樣率
            
        Returns:
            說話者檢測結果
        """
        try:
            # 檢測語音段落
            speech_segments = self.audio_utils.detect_speech_segments(audio_data, sr)
            
            # 提取語音特徵
            speaker_features = self._extract_speaker_features(audio_data, sr, speech_segments)
            
            # 聚類分析（簡化版本）
            speaker_clusters = self._cluster_speakers(speaker_features)
            
            return {
                "success": True,
                "speech_segments": speech_segments,
                "speaker_features": speaker_features,
                "speaker_clusters": speaker_clusters,
                "estimated_speakers": len(speaker_clusters),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_speaker_features(self, audio_data: np.ndarray, sr: int, 
                                speech_segments: List[Tuple[float, float]]) -> List[Dict[str, Any]]:
        """
        提取說話者特徵
        
        Args:
            audio_data: 音訊資料
            sr: 採樣率
            speech_segments: 語音段落列表
            
        Returns:
            特徵列表
        """
        features = []
        
        for start_time, end_time in speech_segments:
            # 提取對應的音訊片段
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment_audio = audio_data[start_sample:end_sample]
            
            if len(segment_audio) > 0:
                # 計算頻譜特徵
                spectral_features = self.audio_utils.calculate_spectral_features(segment_audio, sr)
                
                # 計算額外的說話者特徵
                speaker_features = self._calculate_speaker_specific_features(segment_audio, sr)
                
                features.append({
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time,
                    "spectral_features": spectral_features,
                    "speaker_features": speaker_features,
                    "audio_segment": segment_audio
                })
        
        return features
    
    def _calculate_speaker_specific_features(self, audio_segment: np.ndarray, sr: int) -> Dict[str, float]:
        """
        計算說話者特定特徵
        
        Args:
            audio_segment: 音訊片段
            sr: 採樣率
            
        Returns:
            說話者特徵字典
        """
        # 基本特徵
        rms_energy = np.sqrt(np.mean(audio_segment**2))
        
        # 音調相關特徵（簡化版本）
        if len(audio_segment) > 0:
            # 使用過零率作為音調的粗略估計
            zero_crossings = np.sum(np.diff(np.sign(audio_segment)) != 0)
            pitch_estimate = zero_crossings / (len(audio_segment) / sr)
        else:
            pitch_estimate = 0.0
        
        # 語速相關特徵
        # 這裡使用簡化的方法，實際應用中可能需要更複雜的語音活動檢測
        speech_rate = len(audio_segment) / sr if sr > 0 else 0.0
        
        return {
            "rms_energy": float(rms_energy),
            "pitch_estimate": float(pitch_estimate),
            "speech_rate": float(speech_rate),
            "segment_length": len(audio_segment)
        }
    
    def _cluster_speakers(self, features: List[Dict[str, Any]]) -> List[List[int]]:
        """
        聚類說話者（簡化版本）
        
        Args:
            features: 特徵列表
            
        Returns:
            聚類結果
        """
        if len(features) <= 1:
            return [[0]] if features else []
        
        # 簡化的聚類算法
        # 基於頻譜特徵的相似度進行聚類
        clusters = []
        used_indices = set()
        
        for i, feature in enumerate(features):
            if i in used_indices:
                continue
            
            # 創建新聚類
            cluster = [i]
            used_indices.add(i)
            
            # 尋找相似的特徵
            for j, other_feature in enumerate(features):
                if j in used_indices:
                    continue
                
                # 計算相似度（簡化版本）
                similarity = self._calculate_similarity(feature, other_feature)
                
                if similarity > 0.7:  # 相似度閾值
                    cluster.append(j)
                    used_indices.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def _calculate_similarity(self, feature1: Dict[str, Any], feature2: Dict[str, Any]) -> float:
        """
        計算兩個特徵的相似度
        
        Args:
            feature1: 第一個特徵
            feature2: 第二個特徵
            
        Returns:
            相似度分數 (0-1)
        """
        # 提取頻譜特徵進行比較
        spec1 = feature1["spectral_features"]
        spec2 = feature2["spectral_features"]
        
        # 計算各項特徵的差異
        differences = []
        
        for key in spec1.keys():
            if key in spec2:
                diff = abs(spec1[key] - spec2[key])
                # 正規化差異
                max_val = max(abs(spec1[key]), abs(spec2[key]))
                if max_val > 0:
                    normalized_diff = diff / max_val
                    differences.append(normalized_diff)
        
        if not differences:
            return 0.0
        
        # 計算平均相似度
        avg_difference = np.mean(differences)
        similarity = 1.0 - avg_difference
        
        return max(0.0, min(1.0, similarity))
    
    def assign_speaker_labels(self, speaker_clusters: List[List[int]], 
                            speech_segments: List[Tuple[float, float]]) -> List[Dict[str, Any]]:
        """
        為說話者分配標籤
        
        Args:
            speaker_clusters: 說話者聚類
            speech_segments: 語音段落
            
        Returns:
            帶標籤的語音段落
        """
        labeled_segments = []
        
        for cluster_idx, cluster in enumerate(speaker_clusters):
            speaker_label = f"說話者_{cluster_idx + 1}"
            
            for segment_idx in cluster:
                if segment_idx < len(speech_segments):
                    start_time, end_time = speech_segments[segment_idx]
                    
                    labeled_segments.append({
                        "speaker": speaker_label,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration": end_time - start_time,
                        "cluster_id": cluster_idx
                    })
        
        # 按時間排序
        labeled_segments.sort(key=lambda x: x["start_time"])
        
        return labeled_segments
    
    def generate_speaker_timeline(self, labeled_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成說話者時間軸
        
        Args:
            labeled_segments: 帶標籤的語音段落
            
        Returns:
            說話者時間軸
        """
        timeline = {
            "total_duration": 0.0,
            "speakers": {},
            "segments": labeled_segments
        }
        
        if labeled_segments:
            timeline["total_duration"] = labeled_segments[-1]["end_time"]
        
        # 統計每個說話者的資訊
        for segment in labeled_segments:
            speaker = segment["speaker"]
            
            if speaker not in timeline["speakers"]:
                timeline["speakers"][speaker] = {
                    "total_duration": 0.0,
                    "segment_count": 0,
                    "segments": []
                }
            
            timeline["speakers"][speaker]["total_duration"] += segment["duration"]
            timeline["speakers"][speaker]["segment_count"] += 1
            timeline["speakers"][speaker]["segments"].append(segment)
        
        return timeline 