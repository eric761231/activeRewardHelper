# Google Sheets 權限設定說明

## 問題說明

如果遇到以下錯誤：
```
gspread.exceptions.APIError: {'code': 403, 'message': 'The caller does not have permission', 'status': 'PERMISSION_DENIED'}
```

這表示服務帳號沒有權限訪問 Google Sheet。需要將 Google Sheet 分享給服務帳號。

## 解決步驟

### 1. 確認服務帳號 Email

您的服務帳號 Email 是：
```
active-reward@quickstart-1601643265968.iam.gserviceaccount.com
```

**快速查看方法**：
- 打開 `config/keys/godhash-credentials.json`
- 找到 `"client_email"` 欄位
- 複製該 email 地址

### 2. 分享 Google Sheet 給服務帳號

1. **打開 Google Sheet**：
   - 前往：https://docs.google.com/spreadsheets/d/1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4/edit

2. **點擊右上角的「分享」按鈕**（Share）

3. **在「新增使用者和群組」欄位中**：
   - 輸入服務帳號 Email：`active-reward@quickstart-1601643265968.iam.gserviceaccount.com`
   - **重要**：不要勾選「通知人員」（Notify people），因為這是服務帳號，無法接收通知

4. **設定權限**：
   - 選擇「編輯者」（Editor）權限
   - 這樣服務帳號才能讀取和更新 Sheet 中的資料

5. **點擊「完成」（Done）**

### 3. 驗證權限

完成分享後，等待幾秒鐘讓 Google 更新權限，然後重新執行同步功能。

## 疑難排解

### 問題：分享後仍然出現 403 錯誤

**可能原因**：
1. 權限更新需要時間（通常幾秒到幾分鐘）
2. 服務帳號 Email 輸入錯誤
3. 權限設定為「檢視者」而非「編輯者」

**解決方法**：
1. 等待 1-2 分鐘後重試
2. 確認 Email 地址完全正確（包括 `.iam.gserviceaccount.com` 後綴）
3. 確認權限設定為「編輯者」

### 問題：如何確認服務帳號 Email？

**方法 1：查看憑證檔案**
```bash
# 在 Windows PowerShell 中
Get-Content config\keys\godhash-credentials.json | Select-String "client_email"
```

**方法 2：使用 Python 腳本**
```python
import json
with open('config/keys/godhash-credentials.json', 'r') as f:
    creds = json.load(f)
    print(f"服務帳號 Email: {creds['client_email']}")
```

**方法 3：執行工具腳本**
```bash
python get_service_account_email.py
```

## 重要提醒

1. **服務帳號 Email 是公開的**：這個 Email 可以安全地分享，它只是一個標識符，不會洩露任何敏感資訊。

2. **權限最小化原則**：只給予必要的「編輯者」權限即可，不需要「擁有者」權限。

3. **多個 Sheet**：如果系統需要訪問多個 Google Sheet，需要將每個 Sheet 都分享給服務帳號。

## 相關檔案

- 服務帳號憑證：`config/keys/godhash-credentials.json`
- Google Sheet ID：`1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4`
- 工作表名稱：`神說外交官`

