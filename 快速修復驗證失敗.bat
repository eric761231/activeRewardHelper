@echo off
chcp 65001 >nul
echo ========================================
echo OAuth 驗證失敗 - 快速修復工具
echo ========================================
echo.

echo [步驟 1] 檢查端口 8080 占用情況...
netstat -ano | findstr :8080
echo.

echo [步驟 2] 關閉占用端口 8080 的 Python 進程...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    echo 正在關閉進程 ID: %%a
    taskkill /PID %%a /F >nul 2>&1
    if errorlevel 1 (
        echo   無法關閉進程 %%a（可能需要管理員權限）
    ) else (
        echo   ✓ 已關閉進程 %%a
    )
)
echo.

echo [步驟 3] 刪除舊的令牌檔案...
if exist "config\keys\token.json" (
    del "config\keys\token.json"
    echo   ✓ 已刪除舊令牌
) else (
    echo   ℹ 令牌檔案不存在（正常）
)
echo.

echo [步驟 4] 驗證端口是否已釋放...
timeout /t 2 /nobreak >nul
netstat -ano | findstr :8080
if errorlevel 1 (
    echo   ✓ 端口 8080 已釋放
) else (
    echo   ⚠ 端口 8080 仍被占用，請手動關閉相關程式
)
echo.

echo ========================================
echo 修復完成！
echo ========================================
echo.
echo 下一步：
echo 1. 確認 Google Cloud Console 中的重定向 URI 設定正確
echo 2. 執行: python app.py
echo 3. 觸發同步功能進行 OAuth 授權
echo.
pause

