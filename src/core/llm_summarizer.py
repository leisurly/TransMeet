"""
LLM 摘要分析類別
負責使用大型語言模型進行語音轉文字內容的摘要和分析
"""

import os
import openai
from typing import Dict, List, Optional, Any
from datetime import datetime

from config.settings import Config
from utils.file_utils import FileUtils


class LLMSummarizer:
    """LLM 摘要分析類別"""
    
    def __init__(self):
        """初始化 LLM 摘要器"""
        self.config = Config()
        self.file_utils = FileUtils()
        self.api_key = self.config.get_llm_api_key()
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_summary(self, transcription_text: str, summary_type: str = "general") -> Dict[str, Any]:
        """
        生成轉錄內容摘要
        
        Args:
            transcription_text: 轉錄文字內容
            summary_type: 摘要類型 (general, meeting, interview, lecture)
            
        Returns:
            摘要結果字典
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "未設定 OpenAI API 金鑰"
                }
            
            # 根據摘要類型選擇提示詞
            prompt = self._get_summary_prompt(transcription_text, summary_type)
            
            # 調用 OpenAI API
            response = openai.ChatCompletion.create(
                model=self.config.LLM_SETTINGS["model"],
                messages=[
                    {"role": "system", "content": "你是一個專業的會議記錄摘要助手，能夠準確提取重要資訊並生成結構化的摘要。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.LLM_SETTINGS["max_tokens"],
                temperature=self.config.LLM_SETTINGS["temperature"]
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "summary": summary,
                "summary_type": summary_type,
                "model_used": self.config.LLM_SETTINGS["model"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def extract_key_points(self, transcription_text: str) -> Dict[str, Any]:
        """
        提取關鍵重點
        
        Args:
            transcription_text: 轉錄文字內容
            
        Returns:
            關鍵重點結果
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "未設定 OpenAI API 金鑰"
                }
            
            prompt = f"""
請從以下會議記錄中提取關鍵重點，並以結構化方式呈現：

{transcription_text}

請提供：
1. 主要議題（最多5個）
2. 重要決策（如果有）
3. 行動項目（待辦事項）
4. 關鍵數據或數字
5. 參與者提到的重點

請以繁體中文回答，並使用清晰的格式。
"""
            
            response = openai.ChatCompletion.create(
                model=self.config.LLM_SETTINGS["model"],
                messages=[
                    {"role": "system", "content": "你是一個專業的會議重點提取助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.LLM_SETTINGS["max_tokens"],
                temperature=0.3
            )
            
            key_points = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "key_points": key_points,
                "model_used": self.config.LLM_SETTINGS["model"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_sentiment(self, transcription_text: str) -> Dict[str, Any]:
        """
        分析情感傾向
        
        Args:
            transcription_text: 轉錄文字內容
            
        Returns:
            情感分析結果
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "未設定 OpenAI API 金鑰"
                }
            
            prompt = f"""
請分析以下會議記錄的情感傾向和語氣：

{transcription_text}

請提供：
1. 整體情感傾向（正面/負面/中性）
2. 情感強度（1-10分）
3. 主要情感特徵
4. 語氣分析（正式/非正式/緊張/輕鬆等）
5. 參與者互動模式

請以繁體中文回答。
"""
            
            response = openai.ChatCompletion.create(
                model=self.config.LLM_SETTINGS["model"],
                messages=[
                    {"role": "system", "content": "你是一個專業的情感分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.LLM_SETTINGS["max_tokens"],
                temperature=0.3
            )
            
            sentiment_analysis = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "sentiment_analysis": sentiment_analysis,
                "model_used": self.config.LLM_SETTINGS["model"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_action_items(self, transcription_text: str) -> Dict[str, Any]:
        """
        生成行動項目清單
        
        Args:
            transcription_text: 轉錄文字內容
            
        Returns:
            行動項目結果
        """
        try:
            if not self.api_key:
                return {
                    "success": False,
                    "error": "未設定 OpenAI API 金鑰"
                }
            
            prompt = f"""
請從以下會議記錄中提取所有行動項目（待辦事項）：

{transcription_text}

請以以下格式提供：
1. 行動項目描述
2. 負責人（如果提到）
3. 截止日期（如果提到）
4. 優先級（高/中/低）

如果沒有明確的行動項目，請說明。
"""
            
            response = openai.ChatCompletion.create(
                model=self.config.LLM_SETTINGS["model"],
                messages=[
                    {"role": "system", "content": "你是一個專業的行動項目提取助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.LLM_SETTINGS["max_tokens"],
                temperature=0.3
            )
            
            action_items = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "action_items": action_items,
                "model_used": self.config.LLM_SETTINGS["model"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_summary_prompt(self, text: str, summary_type: str) -> str:
        """
        根據摘要類型生成提示詞
        
        Args:
            text: 轉錄文字
            summary_type: 摘要類型
            
        Returns:
            提示詞
        """
        base_prompt = f"請為以下內容生成{summary_type}摘要：\n\n{text}\n\n"
        
        if summary_type == "meeting":
            return base_prompt + "請包含：會議目的、主要討論內容、決策事項、行動項目。"
        elif summary_type == "interview":
            return base_prompt + "請包含：訪談主題、主要問題、重要回答、關鍵洞察。"
        elif summary_type == "lecture":
            return base_prompt + "請包含：講題、主要概念、重點內容、結論。"
        else:
            return base_prompt + "請提供簡潔明瞭的摘要。"
    
    def save_analysis_results(self, results: Dict, output_path: str) -> bool:
        """
        儲存分析結果
        
        Args:
            results: 分析結果
            output_path: 輸出檔案路徑
            
        Returns:
            是否儲存成功
        """
        return self.file_utils.save_json(results, output_path) 