# OAuth 2.0 設定說明（個人 Google 帳號）

## 概述

系統已改為使用個人 Google 帳號的 OAuth 2.0 認證，而不是服務帳號。這樣可以直接使用您的 Google 帳號來訪問 Google Sheets。

## 設定步驟

### 步驟 1：建立 OAuth 2.0 客戶端 ID

1. **前往 Google Cloud Console**：
   - https://console.cloud.google.com/

2. **選擇或建立專案**：
   - 選擇現有專案，或建立新專案

3. **啟用 Google Sheets API**：
   - 左側選單 → 「API 和服務」→ 「程式庫」
   - 搜尋「Google Sheets API」
   - 點擊「啟用」

4. **建立 OAuth 2.0 客戶端 ID**：
   - 左側選單 → 「API 和服務」→ 「憑證」
   - 點擊「建立憑證」→ 「OAuth 客戶端 ID」
   - 如果第一次使用，需要先設定「OAuth 同意畫面」：
     - 選擇「外部」（除非您有 Google Workspace）
     - 填寫應用程式名稱（例如：「獎勵發放系統」）
     - 選擇您的電子郵件作為支援電子郵件
     - 點擊「儲存並繼續」
     - 在「範圍」頁面，點擊「儲存並繼續」
     - 在「測試使用者」頁面，可以跳過（或添加您的 Google 帳號）
     - 點擊「儲存並繼續」→ 「返回資訊主頁」

5. **建立 OAuth 客戶端 ID**：
   - 應用程式類型：選擇「桌面應用程式」
   - 名稱：輸入名稱（例如：「獎勵發放系統桌面版」）
   - 點擊「建立」

6. **下載憑證檔案**：
   - 點擊下載按鈕（JSON 圖示）
   - 將下載的檔案重新命名為：`client_secrets.json`
   - 放到 `config/keys/` 目錄中

### 步驟 2：更新設定檔

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

**說明**：
- `credentials_file`：OAuth 2.0 客戶端憑證檔案（`client_secrets.json`）
- `token_file`：儲存刷新令牌的檔案（系統會自動建立）

### 步驟 3：第一次授權

1. **啟動後端服務**：
   ```bash
   python app.py
   ```
   或
   ```bash
   start_backend.bat
   ```

2. **第一次運行時**：
   - 系統會自動打開瀏覽器
   - 登入您的 Google 帳號
   - 點擊「允許」授權應用程式訪問 Google Sheets
   - 授權完成後，瀏覽器會顯示「The authentication flow has completed.」
   - 關閉瀏覽器視窗

3. **令牌儲存**：
   - 授權完成後，系統會自動將刷新令牌儲存到 `config/keys/token.json`
   - 之後的運行會自動使用儲存的令牌，不需要再次授權

## 檔案結構

```
config/
├── keys/
│   ├── client_secrets.json    # OAuth 2.0 客戶端憑證（從 Google Cloud Console 下載）
│   └── token.json              # 刷新令牌（系統自動建立，第一次授權後產生）
└── cloud_csv_config.json       # Google Sheets 設定檔
```

## 令牌管理

### 令牌過期處理

- 訪問令牌（Access Token）會自動過期（通常 1 小時）
- 系統會自動使用刷新令牌（Refresh Token）來獲取新的訪問令牌
- 如果刷新令牌也過期，需要重新授權

### 重新授權

如果令牌過期或需要重新授權：

1. **刪除令牌檔案**：
   ```bash
   # Windows
   del config\keys\token.json
   
   # Linux/Mac
   rm config/keys/token.json
   ```

2. **重新啟動應用程式**：
   - 系統會自動觸發授權流程

## 安全性注意事項

1. **保護憑證檔案**：
   - `client_secrets.json` 包含客戶端 ID 和密鑰
   - `token.json` 包含刷新令牌
   - 這些檔案不應該提交到 Git（已在 `.gitignore` 中）

2. **權限範圍**：
   - 系統只請求必要的權限（Google Sheets 和 Drive）
   - 您可以隨時在 Google 帳號設定中撤銷授權

3. **多用戶使用**：
   - 每個用戶需要各自的 `token.json`
   - 如果多人使用，建議使用服務帳號（更適合生產環境）

## 疑難排解

### 問題：找不到 client_secrets.json

**解決方法**：
1. 確認檔案已下載並放到 `config/keys/` 目錄
2. 確認檔案名稱是 `client_secrets.json`
3. 檢查 `config/cloud_csv_config.json` 中的路徑設定

### 問題：授權失敗

**可能原因**：
1. OAuth 同意畫面未設定完成
2. 應用程式類型選擇錯誤（應選擇「桌面應用程式」）
3. 測試使用者未添加（如果應用程式在測試模式）

**解決方法**：
1. 檢查 Google Cloud Console 中的 OAuth 設定
2. 確認應用程式類型是「桌面應用程式」
3. 如果應用程式在測試模式，在「測試使用者」中添加您的 Google 帳號

### 問題：令牌過期

**解決方法**：
1. 刪除 `token.json` 檔案
2. 重新啟動應用程式進行授權

## 與服務帳號的比較

| 特性 | OAuth 2.0（個人帳號） | 服務帳號 |
|------|---------------------|---------|
| 設定複雜度 | 需要 OAuth 流程 | 簡單（只需憑證檔案） |
| 第一次使用 | 需要用戶授權 | 不需要 |
| 令牌管理 | 需要處理刷新 | 自動管理 |
| 適合場景 | 個人使用、開發測試 | 生產環境、自動化 |
| 多用戶 | 每個用戶需要授權 | 共用服務帳號 |

## 切換回服務帳號

如果您想切換回服務帳號：

1. 恢復 `sheets_service.py` 中的服務帳號代碼
2. 更新 `config/cloud_csv_config.json` 使用服務帳號憑證
3. 刪除 `token.json` 檔案

