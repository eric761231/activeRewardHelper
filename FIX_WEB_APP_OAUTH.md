# 修正：網頁應用程式 OAuth 流程

## 問題

您的 `client_secrets.json` 是「**網頁應用程式**」類型（有 `web` 鍵），但代碼使用的是「**桌面應用程式**」流程（`InstalledAppFlow`），兩者不兼容。

## 解決方案選擇

### 方案 A：建立桌面應用程式客戶端（推薦，更簡單）

**優點**：
- ✅ 不需要修改代碼
- ✅ 不需要在 Google Cloud Console 中設定重定向 URI
- ✅ Google 自動允許 localhost

**步驟**：
1. 在 Google Cloud Console 建立新的「桌面應用程式」OAuth 客戶端
2. 下載新的憑證檔案
3. 替換 `config/keys/client_secrets.json`

### 方案 B：修改代碼以支援網頁應用程式（使用現有設定）

**優點**：
- ✅ 可以繼續使用現有的 Google Cloud Console 設定
- ✅ 您已經設定了正確的重定向 URI

**缺點**：
- ❌ 需要修改代碼
- ❌ 需要手動處理重定向 URI

## 實施方案 B：修改代碼支援網頁應用程式

如果您想繼續使用「網頁應用程式」類型，需要修改代碼。

