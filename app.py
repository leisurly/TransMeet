#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TransMeet - 簡化版智能會議記錄語音辨識系統
整合 FastAPI 和現代化首頁介面
"""

import os
import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.requests import Request
from pydantic import BaseModel
import json
from datetime import datetime
import uvicorn
import whisper
import librosa
import numpy as np
import tempfile
import shutil

# 建立必要的目錄
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

class ProcessRequest(BaseModel):
    """處理請求模型"""
    filename: str
    language: str = "zh"
    enable_speaker_detection: bool = False
    enable_llm_analysis: bool = False
    summary_type: str = "meeting"

class TransMeetApp:
    """TransMeet 簡化版應用程式"""
    
    def __init__(self):
        """初始化應用程式"""
        self.app = FastAPI(
            title="TransMeet - 智能會議記錄語音辨識系統",
            description="簡化版語音轉文字系統",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # 設定模板
        self.templates = Jinja2Templates(directory="templates")
        
        # 載入 Whisper 模型
        try:
            self.whisper_model = whisper.load_model("base")
            print("✅ Whisper 模型載入成功")
        except Exception as e:
            print(f"⚠️ Whisper 模型載入失敗: {e}")
            self.whisper_model = None
        
        # 註冊路由
        self._register_routes()
    
    def _register_routes(self):
        """註冊路由"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            """首頁"""
            return self.templates.TemplateResponse("index.html", {"request": request})
        
        @self.app.post("/api/upload")
        async def upload_audio(file: UploadFile = File(...)):
            """處理音訊檔案上傳"""
            try:
                # 驗證檔案格式
                allowed_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
                file_ext = Path(file.filename).suffix.lower()
                
                if file_ext not in allowed_extensions:
                    raise HTTPException(status_code=400, detail="不支援的檔案格式")
                
                # 儲存檔案
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{file.filename}"
                filepath = Path("uploads") / filename
                
                with open(filepath, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                return {
                    "success": True,
                    "filename": filename,
                    "message": "檔案上傳成功"
                }
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/process")
        async def process_audio(request: ProcessRequest):
            """處理音訊檔案"""
            try:
                filepath = Path("uploads") / request.filename
                
                if not filepath.exists():
                    raise HTTPException(status_code=404, detail="檔案不存在")
                
                if not self.whisper_model:
                    raise HTTPException(status_code=500, detail="Whisper 模型未載入")
                
                # 使用 Whisper 進行轉錄
                result = self.whisper_model.transcribe(
                    str(filepath),
                    language=request.language,
                    task="transcribe"
                )
                
                # 準備結果
                transcription_text = result["text"]
                segments = result["segments"]
                
                # 生成摘要（簡單版本）
                summary = self._generate_simple_summary(transcription_text)
                
                # 儲存結果
                results = {
                    'transcription': {
                        'full_text': transcription_text,
                        'segments': segments
                    },
                    'summary': summary,
                    'audio_info': {
                        'filename': request.filename,
                        'duration': segments[-1]['end'] if segments else 0
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                # 儲存到檔案
                results_filename = f"results_{timestamp}_{request.filename}.json"
                results_path = Path("results") / results_filename
                
                with open(results_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                
                return {
                    'success': True,
                    'results': results,
                    'results_file': results_filename
                }
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/download/{filename}")
        async def download_file(filename: str):
            """下載檔案"""
            try:
                filepath = Path("results") / filename
                
                if not filepath.exists():
                    raise HTTPException(status_code=404, detail="檔案不存在")
                
                return FileResponse(
                    path=filepath,
                    filename=filename,
                    media_type='application/octet-stream'
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/health")
        async def health_check():
            """健康檢查"""
            return {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'service': 'TransMeet',
                'whisper_loaded': self.whisper_model is not None
            }
        
        @self.app.get("/api/info")
        async def get_info():
            """取得系統資訊"""
            return {
                'name': 'TransMeet',
                'version': '1.0.0',
                'description': '簡化版智能會議記錄語音辨識系統',
                'features': [
                    '高精度語音轉文字',
                    '多語言支援',
                    '現代化 Web 介面',
                    '檔案下載功能'
                ],
                'supported_formats': ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
            }
    
    def _generate_simple_summary(self, text: str) -> str:
        """生成簡單摘要"""
        if len(text) < 100:
            return text
        
        # 簡單的摘要邏輯：取前200字
        summary = text[:200]
        if len(text) > 200:
            summary += "..."
        
        return summary


def main():
    """主函數"""
    app = TransMeetApp()
    
    # 從環境變數取得配置
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🎤 啟動 TransMeet 應用程式...")
    print(f"🌐 服務地址: http://{host}:{port}")
    print(f"📚 API 文件: http://{host}:{port}/docs")
    print(f"🔧 除錯模式: {debug}")
    
    uvicorn.run(
        app.app,
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )


if __name__ == "__main__":
    main() 