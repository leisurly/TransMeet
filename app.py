#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TransMeet FastAPI 應用程式
整合 OOP 架構的語音轉錄功能和現代化 Web 介面
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
import tempfile
import json
from datetime import datetime
import uvicorn

# 載入環境變數
from dotenv import load_dotenv
load_dotenv()

# 添加 src 目錄到 Python 路徑
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.audio_processor import AudioProcessor
from core.transcription_service import TranscriptionService
from core.speaker_detection import SpeakerDetection
from core.llm_summarizer import LLMSummarizer
from config.settings import Config
from utils.file_utils import FileUtils


class ProcessRequest(BaseModel):
    """處理請求模型"""
    filename: str
    language: str = "zh"
    enable_speaker_detection: bool = True
    enable_llm_analysis: bool = True
    summary_type: str = "meeting"


class TransMeetFastAPI:
    """TransMeet FastAPI 應用程式類別"""
    
    def __init__(self):
        """初始化 FastAPI 應用程式"""
        self.app = FastAPI(
            title="TransMeet - 智能會議記錄語音辨識系統",
            description="基於 OOP 架構的智能語音轉文字系統，整合說話者識別和 LLM 摘要分析",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        self.config = Config()
        self.file_utils = FileUtils()
        
        # 初始化核心服務
        self.audio_processor = AudioProcessor()
        self.transcription_service = TranscriptionService()
        self.speaker_detection = SpeakerDetection()
        self.llm_summarizer = LLMSummarizer()
        
        # 設定模板和靜態檔案
        self.templates = Jinja2Templates(directory="templates")
        
        # 註冊路由
        self._register_routes()
    
    def _register_routes(self):
        """註冊 FastAPI 路由"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            """首頁"""
            return self.templates.TemplateResponse("index.html", {"request": request})
        
        @self.app.post("/api/upload")
        async def upload_audio(file: UploadFile = File(...)):
            """處理音訊檔案上傳"""
            try:
                # 驗證檔案格式
                if not self.config.validate_audio_format(file.filename):
                    raise HTTPException(status_code=400, detail="不支援的檔案格式")
                
                # 儲存檔案
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{file.filename}"
                filepath = self.config.get_upload_path() / filename
                
                # 確保目錄存在
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                # 儲存檔案
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
        async def process_audio(request: ProcessRequest, background_tasks: BackgroundTasks):
            """處理音訊檔案"""
            try:
                filepath = self.config.get_upload_path() / request.filename
                
                if not filepath.exists():
                    raise HTTPException(status_code=404, detail="檔案不存在")
                
                # 1. 音訊處理
                audio_result = self.audio_processor.process_audio_file(str(filepath))
                
                if not audio_result["success"]:
                    raise HTTPException(status_code=500, detail=audio_result['error'])
                
                # 2. 語音轉文字
                transcription_result = self.transcription_service.transcribe_audio(
                    str(filepath),
                    request.language
                )
                
                if not transcription_result["success"]:
                    raise HTTPException(status_code=500, detail=transcription_result['error'])
                
                # 3. 說話者識別
                speaker_result = None
                if request.enable_speaker_detection:
                    speaker_result = self.speaker_detection.detect_speakers(
                        audio_result["audio_data"],
                        audio_result["sample_rate"]
                    )
                
                # 4. LLM 摘要分析
                summary_result = None
                if request.enable_llm_analysis:
                    transcription_text = transcription_result["transcription"]["full_text"]
                    summary_result = self.llm_summarizer.generate_summary(
                        transcription_text,
                        request.summary_type
                    )
                
                # 儲存結果
                results = {
                    'transcription': transcription_result,
                    'speaker_detection': speaker_result,
                    'summary': summary_result,
                    'audio_info': audio_result.get('file_info'),
                    'timestamp': datetime.now().isoformat()
                }
                
                # 儲存到檔案
                results_filename = f"results_{timestamp}_{request.filename}.json"
                results_path = self.config.get_results_path() / results_filename
                self.file_utils.save_json(results, results_path)
                
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
                filepath = self.config.get_results_path() / filename
                
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
                'service': 'TransMeet FastAPI'
            }
        
        @self.app.get("/api/info")
        async def get_info():
            """取得系統資訊"""
            return {
                'name': 'TransMeet',
                'version': '1.0.0',
                'description': '智能會議記錄語音辨識系統',
                'features': [
                    '高精度語音轉文字',
                    '說話者識別',
                    'LLM 摘要分析',
                    '多格式輸出支援'
                ],
                'supported_formats': self.config.AUDIO_SETTINGS['supported_formats']
            }


def main():
    """主函數"""
    app = TransMeetFastAPI()
    
    # 從環境變數取得配置
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🎤 啟動 TransMeet FastAPI 應用程式...")
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