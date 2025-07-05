#!/bin/bash

echo "🎤 TransMeet - 智能會議記錄語音辨識系統"
echo "=========================================="

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安裝，請先安裝 Docker"
    exit 1
fi

# 檢查 Docker Compose 是否安裝
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安裝，請先安裝 Docker Compose"
    exit 1
fi

echo "✅ Docker 環境檢查完成"

# 建立必要目錄
mkdir -p uploads results

echo "🚀 啟動 TransMeet 應用程式..."
echo "🌐 應用程式將在 http://localhost:8000 開啟"
echo "📚 API 文件: http://localhost:8000/docs"
echo "⏹️  按 Ctrl+C 停止應用程式"

# 啟動 Docker Compose
docker compose up --build 