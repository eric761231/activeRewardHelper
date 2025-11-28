# Render 部署完整指南

## 概述

本指南說明如何將後端部署到 Render，並設定 OAuth 2.0 認證。

## 部署步驟

### 步驟 1：準備 OAuth 2.0 憑證

1. **在 Google Cloud Console 建立 Web 應用程式 OAuth 客戶端**：
   - 前往：https://console.cloud.google.com/apis/credentials
   - 建立新的 OAuth 2.0 客戶端 ID
   - **應用程式類型**：選擇「**Web 應用程式**」
   - **授權的重定向 URI**：`https://your-app.onrender.com/oauth2callback`
   - 下載 JSON 檔案，重新命名為 `client_secrets_web.json`

2. **更新設定檔**：
   編輯 `config/cloud_csv_config.json`：
   ```json
   {
       "credentials_file": "keys/client_secrets_web.json",
       "token_file": "keys/token.json",
       "spreadsheet_id": "1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4",
       "worksheet_name": "神說外交官",
       "worksheet_gid": "1753592588"
   }
   ```

### 步驟 2：部署到 Render

1. **前往 Render**：
   - https://render.com/
   - 登入/註冊帳號

2. **建立新的 Web Service**：
   - 點擊 "New +" → "Web Service"
   - 連接您的 GitHub 儲存庫

3. **設定部署**：
   - **Name**: `active-reward-api`（或您喜歡的名稱）
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free（或選擇付費方案）

4. **設定環境變數**：
   - `RENDER`: `true`（用於識別 Render 環境）
   - `RENDER_EXTERNAL_URL`: Render 會自動設定，不需要手動添加
   - `SECRET_KEY`: 設定一個隨機字串（用於 Flask session）

5. **上傳憑證檔案**：
   - 在 Render Dashboard → 您的服務 → Environment
   - 或使用 Render 的 Secrets 功能
   - 將 `client_secrets_web.json` 上傳到 `config/keys/` 目錄
   - **注意**：Render 免費方案不支援持久化檔案系統，建議使用環境變數或 Secrets

### 步驟 3：首次授權

1. **訪問授權 URL**：
   ```
   https://your-app.onrender.com/api/oauth/authorize
   ```

2. **完成授權**：
   - 登入 Google 帳號
   - 點擊「允許」授權
   - 授權完成後會自動重定向並儲存令牌

3. **驗證**：
   - 訪問：`https://your-app.onrender.com/api/status`
   - 應該會顯示系統狀態

### 步驟 4：更新 Netlify 設定

編輯 `netlify/_redirects`，將後端 URL 更新為 Render URL：

```apache
/api/*  https://your-app.onrender.com/api/:splat  200
```

## 重要注意事項

### Render 免費方案限制

1. **檔案系統不持久化**：
   - 每次部署後，檔案系統會重置
   - `token.json` 檔案會遺失
   - **解決方案**：
     - 使用 Render 的環境變數儲存令牌（JSON 字串）
     - 或使用外部儲存（如資料庫）儲存令牌
     - 或每次部署後重新授權

2. **休眠機制**：
   - 15 分鐘無活動後會休眠
   - 首次請求需要較長時間喚醒

### 替代方案：使用服務帳號

如果 OAuth 2.0 在 Render 上設定複雜，建議：

1. **本地開發**：使用 OAuth 2.0（個人帳號）
2. **Render 部署**：使用服務帳號（更簡單、更穩定）

服務帳號的優點：
- 不需要 OAuth 流程
- 令牌不會過期
- 適合自動化運行
- 檔案系統重置不影響

## 疑難排解

### 問題：找不到 client_secrets_web.json

**解決方法**：
1. 確認檔案已上傳到正確位置
2. 檢查 `config/cloud_csv_config.json` 中的路徑設定
3. 使用 Render 的環境變數或 Secrets 功能

### 問題：OAuth 回調失敗

**可能原因**：
1. 重定向 URI 不匹配
2. state 驗證失敗
3. 憑證檔案路徑錯誤

**解決方法**：
1. 確認 Google Cloud Console 中的重定向 URI 完全匹配
2. 檢查 Render 日誌查看詳細錯誤
3. 確認 `RENDER_EXTERNAL_URL` 環境變數正確

### 問題：令牌遺失（部署後）

**原因**：Render 免費方案的檔案系統不持久化

**解決方法**：
1. 使用環境變數儲存令牌
2. 或每次部署後重新授權
3. 或升級到付費方案（支援持久化儲存）

## 快速檢查清單

- [ ] 已建立 Web 應用程式 OAuth 客戶端
- [ ] 已設定重定向 URI：`https://your-app.onrender.com/oauth2callback`
- [ ] 已上傳 `client_secrets_web.json` 到 Render
- [ ] 已設定環境變數 `RENDER=true` 和 `SECRET_KEY`
- [ ] 已部署到 Render
- [ ] 已訪問 `/api/oauth/authorize` 完成授權
- [ ] 已更新 Netlify `_redirects` 指向 Render URL

