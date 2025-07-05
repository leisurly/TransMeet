# 🎤 TransMeet - 用 Breeze-ASR 打造的智慧會議小幫手

嗨，我是 TransMeet 的開發者！👋  
這是一個由我獨立開發的智慧語音會議紀錄系統，結合了語音辨識、說話者識別與 LLM 摘要分析三大功能。  
你只需要上傳一段錄音，它就能幫你轉成逐字稿、自動區分誰說了什麼，並濃縮出會議重點與行動項目，協助你快速掌握整體討論內容。

我特別選用了台灣在地開發的 **Breeze-ASR** 模型，對中文（甚至台語）辨識效果特別好，非常適合給研究團隊、創業小組、教學講座使用。

---

## 💡 為什麼我要做 TransMeet 呢？

最近專題開會非常密集，每次討論都很熱烈，但往往開完會就各忙各的，沒人有時間好好整理逐字稿、會議記錄或摘要內容。

為了讓大家都能清楚掌握討論重點、知道誰負責什麼，我決定打造一個能夠自動幫忙「聽懂」會議內容的智慧小幫手，讓團隊更有效率、更聚焦！

---

## ✨ 主要功能

- **🎯 高精度語音轉文字**：使用 Breeze-ASR 模型進行多語言語音辨識
- **👥 說話者識別**：自動識別和區分不同的說話者
- **🧠 LLM 摘要分析**：使用 OpenAI GPT 進行智能內容摘要
- **📊 詳細分析**：關鍵重點提取、情感分析、行動項目生成
- **💾 多格式輸出**：支援 JSON、SRT 字幕等多種輸出格式
- **🎨 現代化 UI**：基於 Boldo 樣板的美觀首頁設計
- **🔄 雙模式支援**：支援 Streamlit 和 FastAPI 兩種運行模式

---

## 🏗️ 系統架構（Project Structure）

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
├── app.py                        # FastAPI 主應用程式
├── main.py                       # Streamlit 主入口點
├── start.py                      # 統一啟動腳本
├── requirements.txt              # 依賴套件
├── requirements_simple.txt       # 簡化版依賴
├── Dockerfile                    # Docker 配置
├── docker-compose.yaml          # Docker Compose 配置
└── run.sh                       # 啟動腳本
```

---

## 🧪 快速開始（Quick Start）

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動 Streamlit 模式
python start.py --mode streamlit

# 或啟動 FastAPI 模式
python start.py --mode fast
```

---

## 📦 Breeze-ASR 特點

- 🇹🇼 台灣優化模型，對中文語音辨識效果極佳
- 📈 相較 Whisper 更適合在地口語
- 🧑‍💻 支援 CPU & GPU 環境部署

---

## 📄 授權 License

本專案採用 MIT License 授權，歡迎自由使用與修改。

---

## 🤝 貢獻 Contributing

<<<<<<< HEAD
歡迎開 issue 或 pull request 一起完善 TransMeet！

## 🚀 使用指南

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
docker compose up --build

# 背景運行
docker compose up -d
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
