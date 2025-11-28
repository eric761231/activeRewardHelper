"""
環境檢查腳本 - 檢查 Python 環境和已安裝的套件
"""
import sys
import subprocess

print("=" * 60)
print("Python 環境檢查")
print("=" * 60)

# 檢查 Python 版本和路徑
print(f"\n📌 Python 版本: {sys.version}")
print(f"📌 Python 執行檔路徑: {sys.executable}")
print(f"📌 Python 路徑: {sys.path[:3]}...")  # 只顯示前3個路徑

# 檢查必要的套件
print("\n" + "=" * 60)
print("檢查必要套件")
print("=" * 60)

required_packages = [
    'flask',
    'flask_sqlalchemy',
    'sqlalchemy',
    'gspread',
    'google.auth',
    'pymysql',
    'dotenv'
]

missing_packages = []
installed_packages = []

for package in required_packages:
    try:
        if package == 'flask_sqlalchemy':
            __import__('flask_sqlalchemy')
            print(f"✅ {package} - 已安裝")
            installed_packages.append(package)
        elif package == 'google.auth':
            __import__('google.auth')
            print(f"✅ {package} - 已安裝")
            installed_packages.append(package)
        elif package == 'dotenv':
            __import__('dotenv')
            print(f"✅ {package} - 已安裝")
            installed_packages.append(package)
        else:
            __import__(package)
            print(f"✅ {package} - 已安裝")
            installed_packages.append(package)
    except ImportError:
        print(f"❌ {package} - 未安裝")
        missing_packages.append(package)

# 總結
print("\n" + "=" * 60)
print("檢查結果")
print("=" * 60)

if missing_packages:
    print(f"\n⚠️  缺少以下套件: {', '.join(missing_packages)}")
    print("\n請執行以下命令安裝:")
    print(f"python -m pip install {' '.join(missing_packages)}")
    print("\n或安裝所有依賴:")
    print("python -m pip install -r requirements.txt")
else:
    print("\n✅ 所有必要套件都已安裝！")
    print("\n嘗試導入模組...")
    try:
        from models import db, ActiveReward
        print("✅ models 模組導入成功！")
        
        from config import Config
        print("✅ config 模組導入成功！")
        
        from sheets_service import GoogleSheetsService
        print("✅ sheets_service 模組導入成功！")
        
        print("\n🎉 所有模組都可以正常導入！")
    except Exception as e:
        print(f"\n❌ 導入模組時發生錯誤: {e}")
        print(f"錯誤類型: {type(e).__name__}")

print("\n" + "=" * 60)

