# 🎤 TransMeet - 智能會議記錄語音辨識系統

一個基於 OOP 架構的智能語音轉文字系統，整合了說話者識別和 LLM 摘要分析功能，提供現代化的 Boldo 樣板首頁設計。

## ✨ 主要功能

- **🎯 高精度語音轉文字**: 使用 Whisper 模型進行多語言語音辨識
- **👥 說話者識別**: 自動識別和區分不同的說話者
- **🧠 LLM 摘要分析**: 使用 OpenAI GPT 進行智能內容摘要
- **📊 詳細分析**: 關鍵重點提取、情感分析、行動項目生成
- **💾 多格式輸出**: 支援 JSON、SRT 字幕等多種輸出格式
- **🎨 現代化 UI**: 基於 Boldo 樣板的美觀首頁設計
- **🔄 雙模式支援**: 支援 Streamlit 和 Flask 兩種運行模式

## 🏗️ 系統架構

```
TransMeet/
├── src/                          # 核心程式碼 (OOP 架構)
│   ├── core/                     # 核心功能模組
│   │   ├── audio_processor.py    # 音訊處理
│   │   ├── transcription_service.py # 語音轉文字
│   │   ├── speaker_detection.py  # 說話者識別
│   │   └── llm_summarizer.py     # LLM 摘要分析
│   ├── web/                      # Web 介面
│   │   └── app.py               # Streamlit 應用
│   ├── utils/                    # 工具類別
│   │   ├── file_utils.py        # 檔案處理
│   │   └── audio_utils.py       # 音訊工具
│   └── config/                   # 配置設定
│       └── settings.py          # 系統配置
├── templates/                    # HTML 模板
│   └── index.html               # Boldo 樣板首頁
├── uploads/                      # 上傳檔案目錄
├── results/                      # 結果輸出目錄
├── models/                       # 模型檔案目錄
├── main.py                       # Streamlit 主入口點
├── web_app.py                    # Flask 應用程式
├── start.py                      # 統一啟動腳本
├── requirements.txt              # 依賴套件
├── Dockerfile                    # Docker 配置
└── docker-compose.yml           # Docker Compose 配置
```

## 🚀 快速開始

### 1. 環境需求

- Python 3.8+
- CUDA 支援（可選，用於 GPU 加速）

### 2. 安裝依賴

```bash
# 克隆專案
git clone <repository-url>
cd TransMeet

# 安裝依賴
pip install -r requirements.txt
```

### 3. 設定 OpenAI API

```bash
# 設定環境變數
export OPENAI_API_KEY="your-openai-api-key"
```

### 4. 運行應用程式

#### 方式一：使用統一啟動腳本（推薦）

```bash
# 自動選擇最佳模式
python start.py

# 指定 Streamlit 模式
python start.py --mode streamlit

# 指定 Flask 模式
python start.py --mode flask

# 只檢查環境
python start.py --check-only
```

#### 方式二：直接運行

```bash
# Streamlit 模式
streamlit run main.py

# FastAPI 模式
python fastapi_app.py
```

## 🎨 兩種使用者介面

### 1. Boldo 樣板首頁 (FastAPI 模式)
- **網址**: http://localhost:8000
- **特色**: 現代化的響應式設計，專業的企業級外觀
- **功能**: 拖放上傳、即時處理狀態、結果預覽和下載
- **API 文件**: http://localhost:8000/docs

### 2. Streamlit 介面
- **網址**: http://localhost:8501
- **特色**: 互動式數據科學介面，豐富的視覺化功能
- **功能**: 側邊欄配置、即時處理、詳細結果展示

## 📖 使用說明

### 1. 上傳音訊檔案

- 支援格式：WAV, MP3, M4A, FLAC, OGG
- 最大檔案大小：100MB
- 支援拖放上傳

### 2. 設定處理選項

- **語言選擇**: 選擇音訊的主要語言
- **摘要類型**: 選擇適合的摘要類型（會議、訪談、演講等）
- **說話者識別**: 啟用/停用說話者識別功能
- **LLM 分析**: 啟用/停用 LLM 摘要分析

### 3. 查看結果

- **語音轉文字**: 完整的轉錄文字和時間戳記
- **說話者識別**: 說話者統計和時間軸
- **LLM 分析**: 內容摘要、關鍵重點、情感分析、行動項目

### 4. 下載結果

- **JSON 格式**: 完整的處理結果
- **SRT 字幕**: 標準字幕檔案格式
- **TXT 格式**: 純文字轉錄和摘要

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
# 構建並運行
docker-compose up --build

# 背景運行
docker-compose up -d
```

### 使用 Docker

```bash
# 構建映像
docker build -t transmeet .

# 運行容器
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" transmeet
```

## 🔧 配置設定

主要配置檔案：`src/config/settings.py`

```python
# 音訊處理設定
AUDIO_SETTINGS = {
    "sample_rate": 16000,
    "chunk_duration": 30,
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
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "max_tokens": 1000,
    "temperature": 0.7
}
```

## 🎯 核心類別說明

### AudioProcessor
- 負責音訊檔案的載入和預處理
- 提供音訊統計資訊和特徵提取

### TranscriptionService
- 使用 Whisper 模型進行語音轉文字
- 支援時間戳記和字幕生成

### SpeakerDetection
- 識別和區分不同的說話者
- 生成說話者時間軸和統計資訊

### LLMSummarizer
- 使用 OpenAI GPT 進行內容摘要
- 提供關鍵重點提取、情感分析等功能

## 📊 效能優化

### GPU 加速
- 自動檢測 CUDA 可用性
- 支援 GPU 加速的語音轉文字處理

### 記憶體管理
- 自動清理臨時檔案
- 分批處理大型音訊檔案

### 快取機制
- 模型快取避免重複載入
- 結果快取提升響應速度

## 🔒 安全性

- API 金鑰安全儲存
- 檔案上傳驗證
- 臨時檔案自動清理

## 🎨 Boldo 樣板特色

- **響應式設計**: 適配各種螢幕尺寸
- **現代化 UI**: 使用 Bootstrap 5 和 Font Awesome
- **互動效果**: 平滑動畫和過渡效果
- **專業外觀**: 企業級的視覺設計
- **使用者友善**: 直觀的操作流程

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支
3. 提交變更
4. 發起 Pull Request

## 📄 授權

本專案採用 MIT 授權條款。

## 🆘 常見問題

### Q: 如何選擇適合的運行模式？
A: 
- **Streamlit**: 適合數據科學家和開發者，提供豐富的互動功能
- **FastAPI**: 適合一般用戶，提供專業的企業級介面和完整的 API 文件

### Q: 如何提升語音轉文字準確度？
A: 確保音訊品質良好，減少背景噪音，選擇正確的語言設定。

### Q: 說話者識別準確度如何？
A: 目前使用簡化的聚類算法，對於清晰的多說話者音訊效果較好。

### Q: 需要 OpenAI API 金鑰嗎？
A: 只有使用 LLM 摘要分析功能時才需要，基本的語音轉文字功能不需要。

### Q: 支援哪些語言？
A: 支援中文、英文、日文、韓文等多種語言。

## 📞 支援

如有問題或建議，請提交 Issue 或聯繫開發團隊。 

## 總結已完成的清理和重構

### ✅ 已刪除的檔案：
1. **web_app.py** - 已被 FastAPI 替代
2. **boldo-1.0.0/** - 多餘的樣板目錄
3. **README_MultiSpeaker.md** - 舊的說明文件
4. **app.py** - 舊的主應用程式
5. **deploy.sh, setup-containers.sh, run.sh** - 舊的部署腳本
6. **._* 檔案** - macOS 系統檔案

### ✅ 已更新的檔案：
1. **fastapi_app.py** - 新的 FastAPI 應用程式
2. **start.py** - 支援 FastAPI 模式
3. **requirements.txt** - 加入 FastAPI 依賴
4. **Dockerfile** - 更新為 FastAPI 配置
5. **docker-compose.yml** - 更新端口和服務名稱
6. **README.md** - 更新所有 TransMeet 引用
7. **templates/index.html** - 更新品牌名稱
8. **.gitignore** - 完整的忽略規則

### ✅ 已設定的 Git：
1. 初始化 Git 倉庫
2. 設定遠端倉庫為 `git@github.com:leisurly/TransMeet.git`
3. 設定主分支為 `main`

### 🎯 最終專案結構：
```
TransMeet/
├── src/                          # 核心程式碼 (OOP 架構)
├── templates/                    # HTML 模板
├── raw_data/                     # 測試音檔 (保留)
├── models/                       # 模型檔案目錄
├── fastapi_app.py               # FastAPI 應用程式
├── main.py                      # Streamlit 入口點
├── start.py                     # 統一啟動腳本
├── requirements.txt             # 依賴套件
├── Dockerfile                   # Docker 配置
├── docker-compose.yml          # Docker Compose 配置
├── .gitignore                  # Git 忽略規則
└── README.md                   # 專案說明
```

現在您可以執行以下命令來提交到 GitHub：

```bash
<code_block_to_apply_changes_from>
```

專案已經完全重構為 TransMeet，使用 FastAPI 作為主要 Web 框架，並保留了完整的 OOP 架構和功能。 