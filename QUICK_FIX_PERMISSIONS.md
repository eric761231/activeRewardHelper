# 快速修復 Google Sheets 權限問題

## 當前服務帳號

**服務帳號 Email**：`funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com`

## 立即解決步驟

### 步驟 1：打開 Google Sheet

直接點擊此連結：
👉 **https://docs.google.com/spreadsheets/d/1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4/edit**

### 步驟 2：分享給服務帳號

1. **點擊右上角的「分享」按鈕**（藍色按鈕，通常顯示 "Share" 或 "共用"）

2. **在彈出的分享視窗中**：
   - 在「新增使用者和群組」欄位中，**複製貼上以下 Email**：
     ```
     funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com
     ```

3. **設定權限**：
   - 點擊右側的下拉選單
   - **選擇「編輯者」（Editor）**
   - ⚠️ **不要選擇「檢視者」（Viewer）**，這會導致無法更新資料

4. **重要設定**：
   - ❌ **不要勾選「通知人員」**（Notify people）
   - 服務帳號無法接收通知，勾選可能會導致錯誤

5. **點擊「完成」或「傳送」**

### 步驟 3：等待權限生效

- 通常需要 **10-30 秒** 讓 Google 更新權限
- 如果立即測試仍然失敗，請等待 1-2 分鐘後再試

### 步驟 4：重新測試

重新執行同步功能，403 錯誤應該會消失。

## 驗證權限是否設定成功

### 方法 1：檢查分享清單

1. 打開 Google Sheet
2. 點擊「分享」按鈕
3. 在分享清單中查找：`funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com`
4. 確認權限顯示為「編輯者」

### 方法 2：使用測試腳本

```bash
python test_connection.py
```

如果連接成功，會顯示「Google Sheets 連接測試：成功」

## 常見問題

### Q: 分享後仍然出現 403 錯誤？

**A: 可能的原因：**
1. **權限更新需要時間**：等待 1-2 分鐘後重試
2. **Email 輸入錯誤**：確認完全複製貼上，包括 `.iam.gserviceaccount.com` 後綴
3. **權限設定錯誤**：確認設定為「編輯者」，不是「檢視者」
4. **使用了錯誤的服務帳號**：確認憑證檔案中的 email 是 `funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com`

### Q: 如何確認當前使用的服務帳號？

**A: 執行以下命令：**
```bash
python get_service_account_email.py
```

### Q: 建立專案的帳號有權限，為什麼服務帳號沒有？

**A: 這是正常的。** Google Cloud 專案的擁有者權限和 Google Sheet 的分享權限是**分開的**：
- 建立專案的帳號有權限管理 Google Cloud 專案
- 但服務帳號需要**單獨分享**到 Google Sheet 才能訪問

即使建立專案的帳號有 Sheet 的編輯權限，服務帳號也需要被明確分享。

## 快速複製區

**服務帳號 Email**（直接複製）：
```
funotech002@green-bedrock-479611-a8.iam.gserviceaccount.com
```

**Google Sheet 連結**：
```
https://docs.google.com/spreadsheets/d/1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4/edit
```

