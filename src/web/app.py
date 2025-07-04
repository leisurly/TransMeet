"""
會議記錄語音辨識系統 - 主應用程式
整合語音轉文字、說話者識別和LLM摘要分析功能
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# 導入核心模組
from ..core.audio_processor import AudioProcessor
from ..core.transcription_service import TranscriptionService
from ..core.speaker_detection import SpeakerDetection
from ..core.llm_summarizer import LLMSummarizer
from ..config.settings import Config
from ..utils.file_utils import FileUtils


class BreezeASRApp:
    """Breeze ASR 主應用程式類別"""
    
    def __init__(self):
        """初始化應用程式"""
        self.config = Config()
        self.audio_processor = AudioProcessor()
        self.transcription_service = TranscriptionService()
        self.speaker_detection = SpeakerDetection()
        self.llm_summarizer = LLMSummarizer()
        self.file_utils = FileUtils()
        
        # 設定頁面配置
        self._setup_page_config()
        
        # 初始化會話狀態
        self._init_session_state()
    
    def _setup_page_config(self):
        """設定頁面配置"""
        st.set_page_config(
            page_title=self.config.STREAMLIT_SETTINGS["page_title"],
            page_icon=self.config.STREAMLIT_SETTINGS["page_icon"],
            layout=self.config.STREAMLIT_SETTINGS["layout"],
            initial_sidebar_state="expanded"
        )
    
    def _init_session_state(self):
        """初始化會話狀態"""
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = None
        if "transcription_result" not in st.session_state:
            st.session_state.transcription_result = None
        if "speaker_result" not in st.session_state:
            st.session_state.speaker_result = None
        if "summary_result" not in st.session_state:
            st.session_state.summary_result = None
    
    def run(self):
        """運行應用程式"""
        # 顯示標題
        self._display_header()
        
        # 側邊欄
        self._display_sidebar()
        
        # 主要內容區域
        self._display_main_content()
    
    def _display_header(self):
        """顯示頁面標題"""
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #1f77b4; font-size: 2.5rem;">🎤 會議記錄語音辨識系統</h1>
            <p style="font-size: 1.2rem; color: #666;">智能語音轉文字 + LLM 摘要分析</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _display_sidebar(self):
        """顯示側邊欄"""
        with st.sidebar:
            st.header("⚙️ 設定")
            
            # 語言選擇
            language = st.selectbox(
                "選擇語言",
                ["zh", "en", "ja", "ko"],
                index=0,
                help="選擇音訊的主要語言"
            )
            
            # 摘要類型選擇
            summary_type = st.selectbox(
                "摘要類型",
                ["general", "meeting", "interview", "lecture"],
                index=1,
                help="選擇適合的摘要類型"
            )
            
            # LLM 設定
            st.subheader("🤖 LLM 設定")
            api_key = st.text_input(
                "OpenAI API 金鑰",
                type="password",
                help="輸入您的 OpenAI API 金鑰以啟用摘要功能"
            )
            
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                st.success("✅ API 金鑰已設定")
            
            # 處理選項
            st.subheader("🔧 處理選項")
            enable_speaker_detection = st.checkbox(
                "啟用說話者識別",
                value=True,
                help="識別不同的說話者"
            )
            
            enable_llm_analysis = st.checkbox(
                "啟用 LLM 分析",
                value=True,
                help="使用 LLM 進行摘要和分析"
            )
            
            # 儲存設定到會話狀態
            st.session_state.language = language
            st.session_state.summary_type = summary_type
            st.session_state.enable_speaker_detection = enable_speaker_detection
            st.session_state.enable_llm_analysis = enable_llm_analysis
    
    def _display_main_content(self):
        """顯示主要內容"""
        # 檔案上傳區域
        self._display_file_upload()
        
        # 處理結果顯示
        if st.session_state.uploaded_file:
            self._display_processing_results()
    
    def _display_file_upload(self):
        """顯示檔案上傳區域"""
        st.header("📁 上傳音訊檔案")
        
        uploaded_file = st.file_uploader(
            "選擇音訊檔案",
            type=self.config.AUDIO_SETTINGS["supported_formats"],
            help="支援 WAV, MP3, M4A, FLAC, OGG 格式"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            
            # 顯示檔案資訊
            file_info = self.file_utils.get_file_info(uploaded_file.name)
            st.success(f"✅ 檔案已上傳: {uploaded_file.name}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("檔案大小", f"{file_info['size'] / 1024 / 1024:.2f} MB")
            with col2:
                st.metric("檔案類型", file_info['extension'].upper())
            with col3:
                st.metric("上傳時間", file_info['created'][:19])
    
    def _display_processing_results(self):
        """顯示處理結果"""
        if st.button("🚀 開始處理", type="primary"):
            self._process_audio_file()
        
        # 顯示處理結果
        if st.session_state.transcription_result:
            self._display_transcription_results()
        
        if st.session_state.speaker_result:
            self._display_speaker_results()
        
        if st.session_state.summary_result:
            self._display_summary_results()
    
    def _process_audio_file(self):
        """處理音訊檔案"""
        with st.spinner("🔄 正在處理音訊檔案..."):
            # 儲存上傳的檔案
            temp_file = self.file_utils.create_temp_file()
            
            try:
                with open(temp_file, "wb") as f:
                    f.write(st.session_state.uploaded_file.getbuffer())
                
                # 1. 音訊處理
                st.info("📊 正在分析音訊...")
                audio_result = self.audio_processor.process_audio_file(temp_file)
                
                if not audio_result["success"]:
                    st.error(f"音訊處理失敗: {audio_result['error']}")
                    return
                
                # 2. 語音轉文字
                st.info("🎯 正在進行語音轉文字...")
                transcription_result = self.transcription_service.transcribe_audio(
                    temp_file, 
                    st.session_state.language
                )
                
                if transcription_result["success"]:
                    st.session_state.transcription_result = transcription_result
                    st.success("✅ 語音轉文字完成！")
                else:
                    st.error(f"語音轉文字失敗: {transcription_result['error']}")
                    return
                
                # 3. 說話者識別
                if st.session_state.enable_speaker_detection:
                    st.info("👥 正在識別說話者...")
                    speaker_result = self.speaker_detection.detect_speakers(
                        audio_result["audio_data"],
                        audio_result["sample_rate"]
                    )
                    
                    if speaker_result["success"]:
                        st.session_state.speaker_result = speaker_result
                        st.success("✅ 說話者識別完成！")
                    else:
                        st.warning(f"說話者識別失敗: {speaker_result['error']}")
                
                # 4. LLM 摘要分析
                if st.session_state.enable_llm_analysis:
                    st.info("🧠 正在進行 LLM 分析...")
                    transcription_text = transcription_result["transcription"]["full_text"]
                    
                    summary_result = self.llm_summarizer.generate_summary(
                        transcription_text,
                        st.session_state.summary_type
                    )
                    
                    if summary_result["success"]:
                        st.session_state.summary_result = summary_result
                        st.success("✅ LLM 分析完成！")
                    else:
                        st.warning(f"LLM 分析失敗: {summary_result['error']}")
                
                # 儲存結果
                self._save_results()
                
            finally:
                # 清理臨時檔案
                self.file_utils.cleanup_temp_files([temp_file])
    
    def _display_transcription_results(self):
        """顯示轉錄結果"""
        st.header("📝 語音轉文字結果")
        
        result = st.session_state.transcription_result
        transcription = result["transcription"]
        
        # 顯示完整文字
        st.subheader("完整轉錄文字")
        st.text_area(
            "轉錄內容",
            transcription["full_text"],
            height=200,
            disabled=True
        )
        
        # 顯示段落資訊
        st.subheader("段落詳情")
        segments = transcription["segments"]
        
        for i, segment in enumerate(segments[:10]):  # 只顯示前10個段落
            with st.expander(f"段落 {i+1} ({segment['start']:.1f}s - {segment['end']:.1f}s)"):
                st.write(f"**內容:** {segment['text']}")
                st.write(f"**信心度:** {segment['confidence']:.3f}")
        
        # 下載選項
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 下載 JSON"):
                self._download_transcription_json(result)
        
        with col2:
            if st.button("📄 下載字幕"):
                self._download_subtitles(transcription)
    
    def _display_speaker_results(self):
        """顯示說話者識別結果"""
        st.header("👥 說話者識別結果")
        
        result = st.session_state.speaker_result
        
        # 顯示說話者統計
        st.subheader("說話者統計")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("檢測到的說話者", result["estimated_speakers"])
        
        with col2:
            st.metric("語音段落數", len(result["speech_segments"]))
        
        # 顯示說話者時間軸
        if result["speaker_clusters"]:
            st.subheader("說話者時間軸")
            
            # 為說話者分配標籤
            labeled_segments = self.speaker_detection.assign_speaker_labels(
                result["speaker_clusters"],
                result["speech_segments"]
            )
            
            # 生成時間軸
            timeline = self.speaker_detection.generate_speaker_timeline(labeled_segments)
            
            # 顯示每個說話者的資訊
            for speaker, info in timeline["speakers"].items():
                with st.expander(f"{speaker} (總時長: {info['total_duration']:.1f}s)"):
                    st.write(f"**段落數:** {info['segment_count']}")
                    st.write(f"**平均段落時長:** {info['total_duration']/info['segment_count']:.1f}s")
    
    def _display_summary_results(self):
        """顯示摘要分析結果"""
        st.header("🧠 LLM 分析結果")
        
        result = st.session_state.summary_result
        
        if result["success"]:
            # 顯示摘要
            st.subheader("📋 內容摘要")
            st.write(result["summary"])
            
            # 顯示模型資訊
            st.caption(f"使用模型: {result['model_used']}")
            
            # 額外分析選項
            if st.button("🔍 進行額外分析"):
                self._perform_additional_analysis()
        else:
            st.error(f"分析失敗: {result['error']}")
    
    def _perform_additional_analysis(self):
        """執行額外分析"""
        if not st.session_state.transcription_result:
            return
        
        transcription_text = st.session_state.transcription_result["transcription"]["full_text"]
        
        # 創建標籤頁
        tab1, tab2, tab3 = st.tabs(["🔑 關鍵重點", "😊 情感分析", "📋 行動項目"])
        
        with tab1:
            key_points_result = self.llm_summarizer.extract_key_points(transcription_text)
            if key_points_result["success"]:
                st.write(key_points_result["key_points"])
            else:
                st.error(f"提取關鍵重點失敗: {key_points_result['error']}")
        
        with tab2:
            sentiment_result = self.llm_summarizer.analyze_sentiment(transcription_text)
            if sentiment_result["success"]:
                st.write(sentiment_result["sentiment_analysis"])
            else:
                st.error(f"情感分析失敗: {sentiment_result['error']}")
        
        with tab3:
            action_items_result = self.llm_summarizer.generate_action_items(transcription_text)
            if action_items_result["success"]:
                st.write(action_items_result["action_items"])
            else:
                st.error(f"生成行動項目失敗: {action_items_result['error']}")
    
    def _save_results(self):
        """儲存處理結果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = self.config.get_results_path()
        
        # 儲存轉錄結果
        if st.session_state.transcription_result:
            transcription_file = results_dir / f"transcription_{timestamp}.json"
            self.file_utils.save_json(st.session_state.transcription_result, transcription_file)
        
        # 儲存說話者識別結果
        if st.session_state.speaker_result:
            speaker_file = results_dir / f"speaker_{timestamp}.json"
            self.file_utils.save_json(st.session_state.speaker_result, speaker_file)
        
        # 儲存摘要結果
        if st.session_state.summary_result:
            summary_file = results_dir / f"summary_{timestamp}.json"
            self.file_utils.save_json(st.session_state.summary_result, summary_file)
    
    def _download_transcription_json(self, result: Dict[str, Any]):
        """下載轉錄結果 JSON"""
        import json
        
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 下載 JSON 檔案",
            data=json_str,
            file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def _download_subtitles(self, transcription: Dict[str, Any]):
        """下載字幕檔案"""
        srt_content = self.transcription_service.generate_subtitles(transcription, "srt")
        
        st.download_button(
            label="📥 下載 SRT 字幕",
            data=srt_content,
            file_name=f"subtitles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.srt",
            mime="text/plain"
        )


def main():
    """主函數"""
    app = BreezeASRApp()
    app.run()


if __name__ == "__main__":
    main() 