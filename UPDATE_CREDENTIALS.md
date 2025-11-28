# 更新 Google Sheets 憑證檔案說明

## 新的服務帳號資訊

- **服務帳號 Email**：`funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com`
- **專案 ID**：`green-bedrock-479611-a8`

## 更新步驟

### 方法 1：使用新的憑證檔案（推薦）

如果您已經從 Google Cloud Console 下載了新的憑證檔案：

1. **將新的憑證檔案放到正確位置**：
   - 將新憑證檔案複製到：`config/keys/` 目錄
   - 可以重新命名為：`godhash-credentials.json`（覆蓋舊檔案）
   - 或使用新名稱，例如：`funotech-credentials.json`

2. **更新設定檔**（如果使用新檔名）：
   - 編輯 `config/cloud_csv_config.json`
   - 更新 `credentials_file` 欄位：
     ```json
     {
         "credentials_file": "keys/funotech-credentials.json",
         ...
     }
     ```

3. **驗證憑證**：
   ```bash
   python get_service_account_email.py
   ```
   - 應該顯示：`funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com`

### 方法 2：從 Google Cloud Console 下載新憑證

如果還沒有下載新憑證檔案：

1. **前往 Google Cloud Console**：
   - https://console.cloud.google.com/
   - 選擇專案：`green-bedrock-479611-a8`

2. **導航到服務帳號**：
   - 左側選單 → 「IAM 與管理」→ 「服務帳號」
   - 找到服務帳號：`funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com`

3. **下載憑證**：
   - 點擊服務帳號名稱
   - 切換到「金鑰」標籤
   - 點擊「新增金鑰」→ 「建立新金鑰」
   - 選擇「JSON」格式
   - 下載的檔案會自動命名，例如：`green-bedrock-479611-a8-xxxxx.json`

4. **放置憑證檔案**：
   - 將下載的 JSON 檔案重新命名為：`godhash-credentials.json`
   - 放到 `config/keys/` 目錄中（覆蓋舊檔案）

5. **驗證**：
   ```bash
   python get_service_account_email.py
   ```

## 權限確認

由於您提到「用另一個帳號建立專案，這個帳號本身就有編輯試算表的權限」，通常不需要額外分享權限。

但建議確認：
1. 服務帳號 `funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com` 是否有權限
2. 如果仍有 403 錯誤，請將 Google Sheet 分享給服務帳號：
   - 前往：https://docs.google.com/spreadsheets/d/1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4/edit
   - 點擊「分享」→ 輸入服務帳號 Email → 設定為「編輯者」

## 測試連接

更新憑證後，測試連接：
```bash
python test_connection.py
```

或直接啟動後端服務測試同步功能。

