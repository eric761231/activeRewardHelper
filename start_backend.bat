@echo off
chcp 65001 >nul
echo ========================================
echo 啟動獎勵發放系統 - 後端服務
echo ========================================
echo.
echo 正在啟動 Flask 後端服務...
echo 後端將運行在: http://localhost:5000
echo.
echo 請保持此視窗開啟，不要關閉！
echo.
echo 按 Ctrl+C 可以停止服務
echo ========================================
echo.

python app.py

pause

