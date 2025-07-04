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
├── src/
│   ├── core/
│   │   ├── audio_processor.py
│   │   ├── breeze_asr.py
│   │   ├── speaker_detection.py
│   │   └── llm_summarizer.py
│   ├── web/
│   │   └── app.py
│   ├── utils/
│   │   ├── file_utils.py
│   │   └── audio_utils.py
│   └── config/
│       └── settings.py
├── templates/
│   └── index.html
├── uploads/
├── results/
├── main.py
├── web_app.py
├── start.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
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

歡迎開 issue 或 pull request 一起完善 TransMeet！
