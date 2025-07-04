#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TransMeet - 智能會議記錄語音辨識系統
整合語音轉文字、說話者識別和LLM摘要分析功能
"""

import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from web.app import main

if __name__ == "__main__":
    main() 