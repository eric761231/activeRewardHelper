#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具腳本：顯示 Google Sheets 服務帳號 Email
用於快速查看需要分享 Google Sheet 的服務帳號 Email
"""

import json
import sys
from pathlib import Path

def get_service_account_email():
    """從憑證檔案中讀取服務帳號 Email"""
    try:
        # 嘗試從 config.py 讀取設定
        from config import Config
        config = Config()
        credentials_file = Path(config.GOOGLE_SHEETS_CREDENTIALS_FILE)
    except Exception:
        # 如果失敗，使用預設路徑
        base_path = Path(__file__).parent
        credentials_file = base_path / 'config' / 'keys' / 'godhash-credentials.json'
    
    if not credentials_file.exists():
        print(f"錯誤：找不到憑證檔案：{credentials_file}")
        print("\n請確認憑證檔案存在於以下位置之一：")
        print("  - config/keys/godhash-credentials.json")
        print("  - 或 config/cloud_csv_config.json 中指定的路徑")
        sys.exit(1)
    
    try:
        with open(credentials_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
        
        client_email = creds.get('client_email', '')
        project_id = creds.get('project_id', '')
        
        if not client_email:
            print("錯誤：憑證檔案中找不到 client_email")
            sys.exit(1)
        
        print("=" * 60)
        print("Google Sheets 服務帳號資訊")
        print("=" * 60)
        print(f"\n服務帳號 Email：")
        print(f"  {client_email}")
        print(f"\n專案 ID：")
        print(f"  {project_id}")
        print("\n" + "=" * 60)
        print("\n請將此 Email 分享給 Google Sheet，並給予「編輯者」權限。")
        print("\nGoogle Sheet 連結：")
        print("  https://docs.google.com/spreadsheets/d/1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4/edit")
        print("\n" + "=" * 60)
        
        return client_email
        
    except json.JSONDecodeError as e:
        print(f"錯誤：憑證檔案格式錯誤：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"錯誤：讀取憑證檔案失敗：{e}")
        sys.exit(1)

if __name__ == '__main__':
    get_service_account_email()

