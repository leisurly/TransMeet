#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TransMeet 統一啟動腳本
支援 Streamlit 和 Flask 兩種運行模式
"""

import os
import sys
import argparse
from pathlib import Path

def check_dependencies():
    """檢查依賴套件"""
    print("🔍 檢查依賴套件...")
    
    required_packages = [
        'torch', 'transformers', 'librosa', 'soundfile',
        'streamlit', 'flask', 'openai', 'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  缺少以下套件: {', '.join(missing_packages)}")
        print("請執行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依賴套件檢查完成")
    return True

def check_directories():
    """檢查並創建必要目錄"""
    print("📁 檢查目錄結構...")
    
    directories = ['uploads', 'results', 'models', 'templates']
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ 創建目錄: {directory}")
        else:
            print(f"✅ 目錄已存在: {directory}")

def run_streamlit():
    """運行 Streamlit 應用程式"""
    print("🚀 啟動 Streamlit 應用程式...")
    print("🌐 應用程式將在 http://localhost:8501 開啟")
    print("⏹️  按 Ctrl+C 停止應用程式")
    
    os.system("streamlit run main.py --server.port=8501 --server.address=0.0.0.0")

def run_fastapi():
    """運行 FastAPI 應用程式"""
    print("🚀 啟動 FastAPI 應用程式...")
    print("🌐 應用程式將在 http://localhost:8000 開啟")
    print("📚 API 文件: http://localhost:8000/docs")
    print("⏹️  按 Ctrl+C 停止應用程式")
    
    os.system("python fastapi_app.py")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='TransMeet 啟動腳本')
    parser.add_argument(
        '--mode', 
        choices=['streamlit', 'fastapi', 'auto'], 
        default='auto',
        help='選擇運行模式 (預設: auto)'
    )
    parser.add_argument(
        '--check-only', 
        action='store_true',
        help='只檢查環境，不啟動應用程式'
    )
    
    args = parser.parse_args()
    
    print("🎤 TransMeet - 智能會議記錄語音辨識系統")
    print("=" * 50)
    
    # 檢查依賴
    if not check_dependencies():
        sys.exit(1)
    
    # 檢查目錄
    check_directories()
    
    if args.check_only:
        print("\n✅ 環境檢查完成")
        return
    
    # 檢查 OpenAI API 金鑰
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  警告: 未設定 OPENAI_API_KEY 環境變數")
        print("💡 提示: 可以設定環境變數以啟用 LLM 摘要功能")
        print("    export OPENAI_API_KEY='your-api-key'")
    
    print("\n" + "=" * 50)
    
    # 選擇運行模式
    if args.mode == 'auto':
        # 自動選擇模式
        try:
            import streamlit
            print("🎯 自動選擇 Streamlit 模式")
            run_streamlit()
        except ImportError:
            print("🎯 自動選擇 FastAPI 模式")
            run_fastapi()
    elif args.mode == 'streamlit':
        run_streamlit()
    elif args.mode == 'fastapi':
        run_fastapi()

if __name__ == "__main__":
    main() 