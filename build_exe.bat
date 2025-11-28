@echo off
chcp 65001 >nul
echo ========================================
echo 建立獨立可執行檔案 (EXE)
echo ========================================
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python，請確認 Python 已安裝並加入 PATH
    pause
    exit /b 1
)

echo [1/4] 檢查 Python 環境...
python --version
echo.

echo [2/4] 安裝 PyInstaller...
python -m pip install pyinstaller
if errorlevel 1 (
    echo [錯誤] 安裝 PyInstaller 失敗
    pause
    exit /b 1
)
echo.

echo [3/4] 建立 EXE 檔案...
echo 這可能需要幾分鐘時間，請稍候...
echo.

REM 使用 PyInstaller 打包
python -m PyInstaller ^
    --name=activeRewardHelper ^
    --onefile ^
    --console ^
    --add-data "config;config" ^
    --add-data "templates;templates" ^
    --hidden-import=flask_cors ^
    --hidden-import=gspread ^
    --hidden-import=google.oauth2.service_account ^
    --hidden-import=pymysql ^
    --hidden-import=sqlalchemy ^
    --hidden-import=flask_sqlalchemy ^
    --hidden-import=dotenv ^
    --collect-all=flask ^
    --collect-all=gspread ^
    --collect-all=google.auth ^
    app.py

if errorlevel 1 (
    echo [錯誤] 打包失敗
    pause
    exit /b 1
)

echo.
echo [4/4] 完成！
echo.
echo ========================================
echo EXE 檔案位置: dist\activeRewardHelper.exe
echo ========================================
echo.
echo 注意事項：
echo 1. EXE 檔案需要與 config 目錄放在同一資料夾
echo 2. 確保 config\mysql_config.json 和 config\cloud_csv_config.json 存在
echo 3. 確保 config\keys\ 目錄中有 Google 憑證檔案
echo.
pause

