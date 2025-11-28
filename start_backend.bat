@echo off
chcp 65001 >nul
echo ========================================
echo 啟動獎勵發放系統 - 後端服務
echo ========================================
echo.

REM 檢查 Python 是否安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 找不到 Python，請確認 Python 已安裝並加入 PATH
    pause
    exit /b 1
)

echo [1/3] 檢查 Python 環境...
python --version
echo.

echo [2/3] 檢查必要套件...
python -c "import flask_cors" >nul 2>&1
if errorlevel 1 (
    echo [警告] flask-cors 未安裝，正在安裝...
    python -m pip install flask-cors
    if errorlevel 1 (
        echo [錯誤] 安裝 flask-cors 失敗
        pause
        exit /b 1
    )
) else (
    echo [OK] 必要套件已安裝
)
echo.

echo [3/3] 啟動 Flask 後端服務...
echo 後端將運行在: http://localhost:2998
echo.
echo 請保持此視窗開啟，不要關閉！
echo.
echo 按 Ctrl+C 可以停止服務
echo ========================================
echo.

python app.py

pause

