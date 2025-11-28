# OAuth 2.0 在 Render 上的設定說明

## 概述

如果要在 Render 上部署後端，需要使用 **Web 應用程式**類型的 OAuth 2.0 客戶端 ID，而不是桌面應用程式。重定向 URI 需要指向 Render 的 URL。

## 重要區別

### 桌面應用程式（當前實現）
- 使用 `InstalledAppFlow` 和 `run_local_server()`
- 重定向 URI：`http://localhost:8080` 等本地 URI
- 適合：本地開發、EXE 執行檔

### Web 應用程式（Render 部署）
- 使用 `Flow` 和 Web 重定向
- 重定向 URI：`https://your-app.onrender.com/oauth2callback`
- 適合：雲端部署、Web 服務

## 設定步驟

### 步驟 1：在 Google Cloud Console 建立 Web 應用程式 OAuth 客戶端

1. **前往 Google Cloud Console**：
   - https://console.cloud.google.com/apis/credentials

2. **建立新的 OAuth 2.0 客戶端 ID**：
   - 點擊「建立憑證」→ 「OAuth 客戶端 ID」
   - **應用程式類型**：選擇「**Web 應用程式**」（不是桌面應用程式）
   - **名稱**：輸入名稱（例如：「獎勵發放系統 Web 版」）

3. **設定授權的重定向 URI**：
   - 在「授權的重定向 URI」區段，點擊「新增 URI」
   - 輸入您的 Render URL + 回調路徑：
     ```
     https://your-app.onrender.com/oauth2callback
     ```
   - 例如：`https://active-reward-api.onrender.com/oauth2callback`
   - **注意**：必須使用 HTTPS（Render 提供 HTTPS）

4. **儲存並下載憑證**：
   - 點擊「建立」
   - 下載 JSON 檔案
   - 重新命名為 `client_secrets_web.json`（與桌面版區分）

### 步驟 2：代碼已修改完成 ✅

代碼已經修改完成，現在支援：
- **桌面應用程式流程**：本地開發和 EXE 執行檔
- **Web 應用程式流程**：Render 等雲端平台

系統會根據環境變數自動選擇使用哪種流程。

#### 新增的功能

1. **`/api/oauth/authorize`** - 啟動 OAuth 授權流程（Web 環境）
2. **`/oauth2callback`** - OAuth 回調處理（接收 Google 授權結果）

#### 自動環境偵測

- 如果偵測到 `RENDER` 環境變數或 `WEB_OAUTH=true`，使用 Web 流程
- 否則使用桌面應用程式流程（本地開發）

### 步驟 3：在 Render 上設定環境變數

1. 前往 Render Dashboard → 您的服務 → Environment
2. 添加環境變數：
   - `RENDER`: `true`（用於識別 Render 環境）
   - `RENDER_EXTERNAL_URL`: `https://your-app.onrender.com`（您的 Render URL）

### 步驟 4：更新設定檔

在 `config/cloud_csv_config.json` 中：

```json
{
    "credentials_file": "keys/client_secrets_web.json",
    "token_file": "keys/token.json",
    "spreadsheet_id": "1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4",
    "worksheet_name": "神說外交官",
    "worksheet_gid": "1753592588"
}
```

## 使用流程

### 在 Render 上首次使用

1. **部署到 Render**：
   - 確保已設定環境變數 `RENDER_EXTERNAL_URL`（Render 會自動設定）
   - 上傳 `client_secrets_web.json` 到 `config/keys/` 目錄

2. **啟動授權流程**：
   - 訪問：`https://your-app.onrender.com/api/oauth/authorize`
   - 或訪問首頁，如果沒有授權，系統會提示訪問授權 URL

3. **完成授權**：
   - 瀏覽器會重定向到 Google 登入頁面
   - 登入您的 Google 帳號
   - 點擊「允許」授權應用程式
   - 授權完成後，會自動重定向回 `/oauth2callback`
   - 系統會儲存令牌到 `config/keys/token.json`

4. **之後的使用**：
   - 系統會自動使用儲存的令牌
   - 如果令牌過期，會自動刷新
   - 如果刷新失敗，需要重新授權

### 本地開發

- 繼續使用桌面應用程式類型的 OAuth 客戶端
- 使用 `client_secrets.json`（桌面版）
- 啟動應用程式時，如果沒有授權，會自動打開瀏覽器進行授權

## 注意事項

1. **兩個 OAuth 客戶端**：
   - 桌面應用程式：用於本地開發和 EXE
   - Web 應用程式：用於 Render 部署

2. **憑證檔案**：
   - `client_secrets.json` - 桌面版
   - `client_secrets_web.json` - Web 版

3. **重定向 URI 必須完全匹配**：
   - 必須包含完整的 URL（包括 `https://`）
   - 路徑必須完全一致（例如：`/oauth2callback`）

4. **安全性**：
   - 不要在程式碼中硬編碼重定向 URI
   - 使用環境變數動態設定

## 簡化方案：使用服務帳號

如果 OAuth 2.0 在 Render 上設定複雜，可以考慮：

1. **本地開發**：使用 OAuth 2.0（個人帳號）
2. **Render 部署**：使用服務帳號（更簡單、更穩定）

這樣可以避免在 Render 上處理 OAuth 流程的複雜性。

