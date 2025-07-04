"""
檔案處理工具類別
提供檔案操作相關的實用功能
"""

import os
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
import shutil


class FileUtils:
    """檔案處理工具類別"""
    
    @staticmethod
    def save_json(data: Dict, filepath: Union[str, Path]) -> bool:
        """
        儲存 JSON 檔案
        
        Args:
            data: 要儲存的資料
            filepath: 檔案路徑
            
        Returns:
            是否儲存成功
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"儲存 JSON 檔案失敗: {e}")
            return False
    
    @staticmethod
    def load_json(filepath: Union[str, Path]) -> Optional[Dict]:
        """
        載入 JSON 檔案
        
        Args:
            filepath: 檔案路徑
            
        Returns:
            JSON 資料或 None
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"載入 JSON 檔案失敗: {e}")
            return None
    
    @staticmethod
    def create_temp_file(suffix: str = ".wav") -> str:
        """
        創建臨時檔案
        
        Args:
            suffix: 檔案副檔名
            
        Returns:
            臨時檔案路徑
        """
        return tempfile.mktemp(suffix=suffix)
    
    @staticmethod
    def get_file_info(filepath: Union[str, Path]) -> Dict:
        """
        取得檔案資訊
        
        Args:
            filepath: 檔案路徑
            
        Returns:
            檔案資訊字典
        """
        path = Path(filepath)
        stat = path.stat()
        
        return {
            "filename": path.name,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": path.suffix.lower()
        }
    
    @staticmethod
    def cleanup_temp_files(temp_files: List[str]) -> None:
        """
        清理臨時檔案
        
        Args:
            temp_files: 臨時檔案路徑列表
        """
        for filepath in temp_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"清理臨時檔案失敗 {filepath}: {e}")
    
    @staticmethod
    def ensure_directory(directory: Union[str, Path]) -> Path:
        """
        確保目錄存在
        
        Args:
            directory: 目錄路徑
            
        Returns:
            目錄路徑物件
        """
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def get_unique_filename(directory: Union[str, Path], filename: str) -> str:
        """
        取得唯一檔案名稱
        
        Args:
            directory: 目錄路徑
            filename: 原始檔案名稱
            
        Returns:
            唯一檔案名稱
        """
        path = Path(directory) / filename
        counter = 1
        
        while path.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            new_filename = f"{stem}_{counter}{suffix}"
            path = Path(directory) / new_filename
            counter += 1
        
        return path.name 