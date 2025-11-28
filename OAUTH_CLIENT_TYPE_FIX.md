# OAuth 客戶端類型錯誤修正指南

## 問題診斷

從您的 Google Cloud Console 截圖可以看到，您使用的是「**網頁應用程式**」類型的 OAuth 客戶端 ID，但我們的代碼使用的是「**桌面應用程式**」流程。

## 兩種類型的區別

### 桌面應用程式（Desktop Application）
- **使用**：`InstalledAppFlow`
- **重定向 URI**：不需要在 Google Cloud Console 中設定（Google 自動允許 localhost）
- **適合**：本地開發、EXE 執行檔
- **代碼**：`flow.run_local_server(port=8080)`

### 網頁應用程式（Web Application）
- **使用**：`Flow`
- **重定向 URI**：必須在 Google Cloud Console 中明確設定
- **適合**：Web 服務、Render 部署
- **代碼**：需要手動處理授權流程和回調

## 解決方案

### 方案 1：建立桌面應用程式客戶端（推薦，適合本地開發）

1. **在 Google Cloud Console 建立新的 OAuth 客戶端**：
   - 前往：https://console.cloud.google.com/apis/credentials
   - 點擊「建立憑證」→ 「OAuth 客戶端 ID」
   - **應用程式類型**：選擇「**桌面應用程式**」（不是網頁應用程式）
   - **名稱**：輸入名稱（例如：「獎勵發放系統桌面版」）
   - 點擊「建立」

2. **下載憑證檔案**：
   - 點擊下載按鈕（JSON 圖示）
   - 將下載的檔案重新命名為：`client_secrets.json`
   - 放到 `config/keys/` 目錄中

3. **更新設定檔**：
   編輯 `config/cloud_csv_config.json`：
   ```json
   {
       "credentials_file": "keys/client_secrets.json",
       "token_file": "keys/token.json",
       "spreadsheet_id": "1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4",
       "worksheet_name": "神說外交官",
       "worksheet_gid": "1753592588"
   }
   ```

4. **重要**：桌面應用程式不需要在 Google Cloud Console 中設定「已授權的重新導向 URI」，Google 會自動允許 localhost。

### 方案 2：繼續使用網頁應用程式客戶端（需要修改代碼）

如果您想繼續使用「網頁應用程式」類型，需要：

1. **確保「已授權的重新導向 URI」中有正確的 URI**：
   - 您已經添加了：
     - `http://localhost`
     - `http://localhost:8080`
     - `http://127.0.0.1`
     - `http://127.0.0.1:8080`
   - ✅ 這些設定是正確的

2. **修改代碼以使用 Web 應用程式流程**：
   - 需要將 `InstalledAppFlow` 改為 `Flow`
   - 需要手動處理重定向 URI
   - 這會讓代碼變得更複雜

## 推薦方案

**建議使用方案 1（桌面應用程式）**，因為：
- ✅ 代碼已經為桌面應用程式優化
- ✅ 不需要在 Google Cloud Console 中設定重定向 URI
- ✅ 更簡單，自動處理 localhost 回調
- ✅ 適合本地開發和 EXE 執行檔

## 快速檢查

### 檢查當前使用的客戶端類型

1. 打開 `config/keys/client_secrets.json`
2. 查看檔案結構：
   - **桌面應用程式**：有 `installed` 鍵
     ```json
     {
       "installed": {
         "client_id": "...",
         "client_secret": "..."
       }
     }
     ```
   - **網頁應用程式**：有 `web` 鍵
     ```json
     {
       "web": {
         "client_id": "...",
         "client_secret": "...",
         "redirect_uris": [...]
       }
     }
     ```

### 如果發現類型不匹配

- **情況 1**：憑證檔案是「網頁應用程式」類型，但代碼使用桌面流程
  - **解決**：建立新的「桌面應用程式」客戶端，下載新憑證

- **情況 2**：憑證檔案是「桌面應用程式」類型，但 Google Cloud Console 顯示「網頁應用程式」
  - **解決**：確認您查看的是正確的客戶端 ID

## 驗證

完成後，重新運行應用程式：

1. 刪除舊的令牌：
   ```bash
   del config\keys\token.json
   ```

2. 重新啟動：
   ```bash
   python app.py
   ```

3. 應該會成功：
   - 瀏覽器自動打開
   - 可以正常登入和授權
   - 不再出現 `redirect_uri_mismatch` 錯誤

