"""
測試腳本：用於驗證 Google Sheets 和資料庫連接
"""
import sys
from config import Config
from models import db
from sheets_service import GoogleSheetsService

def test_database():
    """測試資料庫連接"""
    print("=" * 50)
    print("測試資料庫連接...")
    print("=" * 50)
    
    try:
        config = Config()
        from flask import Flask
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
        db.init_app(app)
        
        with app.app_context():
            # 測試連接
            db.session.execute(db.text("SELECT 1"))
            print("✅ 資料庫連接成功！")
            
            # 檢查資料表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'active_reward' in tables:
                print("✅ active_reward 資料表存在")
                
                # 計算記錄數
                from models import ActiveReward
                count = ActiveReward.query.count()
                print(f"📊 目前資料表中有 {count} 筆記錄")
            else:
                print("⚠️  active_reward 資料表不存在，將在首次執行時自動建立")
            
            return True
    except Exception as e:
        print(f"❌ 資料庫連接失敗: {str(e)}")
        print("\n請檢查：")
        print("1. 資料庫服務是否正在運行")
        print("2. .env 檔案中的資料庫設定是否正確")
        print("3. 資料庫使用者是否有足夠權限")
        return False

def test_google_sheets():
    """測試 Google Sheets 連接"""
    print("\n" + "=" * 50)
    print("測試 Google Sheets 連接...")
    print("=" * 50)
    
    try:
        service = GoogleSheetsService()
        print("✅ Google Sheets 連接成功！")
        print(f"📄 當前工作表名稱: {service.worksheet.title}")
        
        # 檢查是否找到正確的工作表
        config = Config()
        if hasattr(config, 'WORKSHEET_NAME') and config.WORKSHEET_NAME:
            if service.worksheet.title == config.WORKSHEET_NAME:
                print(f"✅ 成功找到指定工作表: {config.WORKSHEET_NAME}")
            else:
                print(f"⚠️  當前工作表名稱 ({service.worksheet.title}) 與設定檔中的名稱 ({config.WORKSHEET_NAME}) 不符")
        
        # 列出所有可用的工作表
        print(f"\n📋 試算表中的所有工作表:")
        for idx, sheet in enumerate(service.spreadsheet.worksheets(), 1):
            marker = " ← 當前使用" if sheet.title == service.worksheet.title else ""
            print(f"   {idx}. {sheet.title} (GID: {sheet.id}){marker}")
        
        # 讀取標題列
        all_values = service.worksheet.get_all_values()
        if all_values:
            headers = all_values[0]
            print(f"📋 欄位名稱: {', '.join(headers)}")
            
            # 檢查「已發放」欄位
            issued_found = False
            
            for header in headers:
                if '已發放' in header or 'issued' in header.lower():
                    issued_found = True
                    print(f"✅ 找到「已發放」欄位: {header}")
            
            if not issued_found:
                print("⚠️  未找到「已發放」欄位（欄位名稱需包含「已發放」或「issued」）")
            
            # 檢查必要的欄位
            required_fields = ['執行代號', '角色身分證', '角色ID', '道具編號', '補償道具名稱', '數量']
            found_fields = []
            missing_fields = []
            
            for field in required_fields:
                found = False
                for header in headers:
                    if field in header:
                        found_fields.append(header)
                        found = True
                        break
                if not found:
                    missing_fields.append(field)
            
            if found_fields:
                print(f"\n✅ 找到必要欄位: {', '.join(found_fields)}")
            if missing_fields:
                print(f"⚠️  缺少必要欄位: {', '.join(missing_fields)}")
            
            # 檢查資料列數
            data_rows = len(all_values) - 1  # 減去標題列
            print(f"📊 資料列數（不含標題）: {data_rows}")
            
            # 測試讀取未確認資料
            unconfirmed_rows, headers, confirmed_col_idx = service.get_unconfirmed_rows()
            print(f"📝 未確認的資料列數: {len(unconfirmed_rows)}")
        
        return True
    except FileNotFoundError:
        print("❌ 找不到 credentials.json 檔案")
        print("\n請檢查：")
        print("1. credentials.json 檔案是否存在於專案根目錄")
        print("2. 檔案名稱是否正確")
        return False
    except Exception as e:
        print(f"❌ Google Sheets 連接失敗: {str(e)}")
        print("\n請檢查：")
        print("1. credentials.json 檔案格式是否正確")
        print("2. 是否已啟用 Google Sheets API 和 Google Drive API")
        print("3. 是否已將試算表分享給服務帳號的電子郵件")
        return False

if __name__ == '__main__':
    print("\n🔍 開始測試系統連接...\n")
    
    db_ok = test_database()
    sheets_ok = test_google_sheets()
    
    print("\n" + "=" * 50)
    print("測試結果總結")
    print("=" * 50)
    
    if db_ok and sheets_ok:
        print("✅ 所有連接測試通過！系統已準備就緒。")
        sys.exit(0)
    else:
        print("❌ 部分測試失敗，請檢查上述錯誤訊息。")
        sys.exit(1)

