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

- **🎯 高精度語音轉文字**：使用 Whisper 模型進行多語言語音辨識
- **👥 說話者識別**：自動識別和區分不同的說話者
- **🧠 LLM 摘要分析**：使用 OpenAI GPT 進行智能內容摘要
- **📊 詳細分析**：關鍵重點提取、情感分析、行動項目生成
- **💾 多格式輸出**：支援 JSON、SRT 字幕等多種輸出格式
- **🎨 現代化 UI**：基於 Boldo 樣板的美觀首頁設計
- **🚀 FastAPI 架構**：高效能的 RESTful API 設計

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
│   ├── utils/                    # 工具類別
│   │   ├── file_utils.py        # 檔案處理
│   │   └── audio_utils.py       # 音訊工具
│   └── config/                   # 配置設定
│       └── settings.py          # 系統配置
├── templates/                    # HTML 模板
│   └── index.html               # Boldo 樣板首頁
├── models/                       # 模型檔案目錄
├── raw_data/                     # 測試音檔 (保留)
├── app.py                        # FastAPI 主應用程式
├── requirements.txt              # 依賴套件
├── Dockerfile                    # Docker 配置
├── docker-compose.yaml          # Docker Compose 配置
├── run.sh                       # 啟動腳本
└── .gitignore                   # Git 忽略規則
```

---

## 🧪 快速開始（Quick Start）

### 環境設定

1. **複製環境變數範例檔案**：
```bash
cp .env.example .env
```

2. **編輯 .env 檔案**：
```bash
# 編輯 .env 檔案，填入你的 OpenAI API 金鑰
nano .env
```

**重要**：如果你要使用 LLM 摘要分析功能，需要設定 `OPENAI_API_KEY`。
如果沒有設定，基本的語音轉文字功能仍可正常運作。

### 使用 Docker（推薦）

```bash
# 構建並運行
docker compose up --build

# 背景運行
docker compose up -d
```

### 本地開發

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動應用程式
python app.py

# 或使用啟動腳本
./run.sh
```

---

## 📦 技術特點

- 🇹🇼 支援中文語音辨識，效果極佳
- 📈 使用 Whisper 模型，準確度高
- 🧑‍💻 支援 CPU & GPU 環境部署
- 🏗️ 完整的 OOP 架構設計
- 🚀 FastAPI 高效能 Web 框架

---

## 📄 授權 License

本專案採用 MIT License 授權，歡迎自由使用與修改。

---

## 🤝 貢獻 Contributing

歡迎開 issue 或 pull request 一起完善 TransMeet！
