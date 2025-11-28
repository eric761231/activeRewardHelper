# 快速設定指南

## 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

## 2. 設定 Google Sheets API

### 步驟 A：建立 Google Cloud 專案
1. 前往 https://console.cloud.google.com/
2. 建立新專案或選擇現有專案
3. 啟用以下 API：
   - Google Sheets API
   - Google Drive API

### 步驟 B：建立服務帳號
1. 前往「IAM 與管理」>「服務帳號」
2. 點擊「建立服務帳號」
3. 輸入服務帳號名稱（例如：sheets-reader）
4. 點擊「建立並繼續」
5. 跳過角色設定，直接點擊「完成」

### 步驟 C：下載憑證
1. 在服務帳號列表中，點擊剛建立的服務帳號
2. 前往「金鑰」標籤
3. 點擊「新增金鑰」>「建立新金鑰」
4. 選擇「JSON」格式
5. 下載的檔案重新命名為 `credentials.json`
6. 將 `credentials.json` 放在專案根目錄

### 步驟 D：分享試算表
1. 開啟您的 Google Sheets
2. 點擊右上角的「共用」按鈕
3. 輸入服務帳號的電子郵件（在 credentials.json 中的 `client_email` 欄位）
4. 給予「編輯者」權限
5. 點擊「完成」

## 3. 設定資料庫

### 建立資料庫和資料表

```sql
CREATE DATABASE active_reward_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE active_reward_db;

CREATE TABLE active_reward (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    amount DECIMAL(10, 2),
    status VARCHAR(50),
    confirmed VARCHAR(10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 4. 設定環境變數

在專案根目錄建立 `.env` 檔案：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=active_reward_db

GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4
WORKSHEET_GID=1753592588

SECRET_KEY=your-secret-key-here
```

## 5. 啟動應用程式

```bash
python app.py
```

然後在瀏覽器中開啟：http://localhost:5000

## 試算表欄位要求

您的 Google Sheets 需要包含以下欄位（欄位名稱可以不同，但需要包含關鍵字）：

- **已確認欄位**：欄位名稱需包含「確認」、「confirmed」或「已確認」
- **發放需要再確認欄位**：欄位名稱需包含「發放需要再確認」或「need_confirm」

系統會自動偵測這些欄位，並只處理「已確認」欄位不是 "V" 的資料列。

## 常見問題

### Q: 如何確認服務帳號的電子郵件？
A: 開啟 `credentials.json` 檔案，找到 `client_email` 欄位，那就是服務帳號的電子郵件。

### Q: 如何找到試算表的 GID？
A: 在 Google Sheets 的網址中，`#gid=1753592588` 後面的數字就是 GID。

### Q: 資料沒有寫入資料庫？
A: 請檢查：
1. 資料庫連線設定是否正確
2. 試算表中是否有未確認的資料（已確認欄位不是 V）
3. 查看終端機的錯誤訊息

