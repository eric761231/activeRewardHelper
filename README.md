# activeRewardHelper

簡短說明：這個專案為一個小型後端服務（Flask）用來從 Google Sheets 同步補償資料到 MySQL，並提供一個簡單的前端介面（`templates/index.html`）用於觸發同步。

重要（安全）
- 請勿把 `config/keys/*.json`（Google service account）或 `config/mysql_config.json` 推到公開的 GitHub。這些檔案已加入 `.gitignore`。

本地快速啟動
1. 建立 Python virtualenv 並安裝依賴
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```
2. 將你的 service account JSON 放到 `config/keys/`，並在 `config/cloud_csv_config.json` 中設定 `credentials_file` 的路徑（例如 `config/keys/godhash-credentials.json`）。
3. 調整 MySQL 設定（如果需要）在 `config/mysql_config.json`。
4. 啟動應用
```powershell
python app.py
```

測試 API
- 檢查狀態： `GET /api/status`
- 執行同步： `POST /api/sync`

部署前端到 Netlify（快速測試）
1. 在 Netlify 建立站點，連 Github repo（此 repo 或獨立 UI repo）。
2. 使用本 repo 的 `_redirects` 來代理 `/api/*` 到你的後端（或 ngrok）。

若需我幫忙：請貼出你想用的 GitHub repo URL 或允許我提供 `git` 指令，我會給出精準的 push 步驟。

---
作者：your team
# 獎勵發放系統 (Active Reward Helper)

這是一個自動化系統，用於將 Google Sheets 的資料同步到資料庫，並自動更新確認狀態。

## 功能特色

1. ✅ 從 Google Sheets 讀取未確認的資料
2. ✅ 自動將資料寫入 `active_reward` 資料表
3. ✅ 自動更新 Google Sheets 的確認欄位為 "V"
4. ✅ 只處理尚未確認的資料（已確認欄位不是 V）
5. ✅ 響應式 Web UI，支援手機和電腦操作
6. ✅ 即時回報處理結果

## 系統需求

- Python 3.8 或更高版本
- MySQL 資料庫
- Google Cloud 專案（用於 Google Sheets API）

## 安裝步驟

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2. 設定 Google Sheets API

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google Sheets API 和 Google Drive API
4. 建立服務帳號：
   - 前往「IAM 與管理」>「服務帳號」
   - 建立新的服務帳號
   - 下載 JSON 憑證檔案
5. 將憑證檔案重新命名為 `credentials.json` 並放在專案根目錄
6. 分享 Google Sheets 給服務帳號的電子郵件（在試算表中點擊「共用」）

### 3. 設定資料庫

建立 MySQL 資料庫和資料表：

```sql
CREATE DATABASE active_reward_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE active_reward_db;

CREATE TABLE active_reward (
    id INT AUTO_INCREMENT PRIMARY KEY,
    round INT,
    char_id VARCHAR(255),
    char_name VARCHAR(255),
    item_id VARCHAR(255),
    item_name VARCHAR(255),
    item_count INT,
    item_obj_id INT DEFAULT 0,
    item_enchant INT DEFAULT 0,
    materials INT DEFAULT 0,
    materials_count INT DEFAULT 0,
    exp INT DEFAULT 0,
    state INT DEFAULT 1,
    end_time DATETIME
);
```

### 4. 設定環境變數

建立 `.env` 檔案（參考 `.env.example`）：

```env
# 資料庫設定
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=active_reward_db

# Google Sheets API 設定
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4
WORKSHEET_GID=1753592588

# Flask 設定（可選）
SECRET_KEY=your-secret-key-here
```

## 使用方式

### 啟動應用程式

```bash
python app.py
```

應用程式會在 `http://localhost:5000` 啟動。

### 使用介面

1. 在瀏覽器中開啟 `http://localhost:5000`
2. 點擊「開始發放」按鈕
3. 系統會自動：
   - 讀取 Google Sheets 中未確認的資料
   - 將資料寫入資料庫
   - 更新試算表的確認欄位為 "V"
4. 完成後會顯示「發放完成」訊息

## 試算表欄位說明

系統會自動偵測以下欄位：

- **已發放欄位**：包含「已發放」或「issued」的欄位名稱（用於判斷是否已處理）

### 欄位對應

試算表欄位與資料庫欄位的對應關係：

| 試算表欄位 | 資料庫欄位 | 說明 |
|-----------|-----------|------|
| 執行代號 | round | 整數 |
| 角色身分證 | char_id | 字串 |
| 角色ID | char_name | 字串 |
| 道具編號 | item_id | 字串 |
| 補償道具名稱 | item_name | 字串 |
| 數量 | item_count | 整數 |
| 已發放 | state | 處理後設為 1（已發放） |

系統會自動將「已發放」欄位不是 'V' 的資料寫入資料庫，並將試算表中的「已發放」欄位更新為 'V'。

## 專案結構

```
activeRewardHelper/
├── app.py                 # Flask 應用程式主程式
├── config.py              # 設定檔
├── models.py              # 資料庫模型
├── sheets_service.py      # Google Sheets 服務
├── sync_service.py        # 資料同步服務
├── requirements.txt       # Python 依賴套件
├── .env                   # 環境變數（需自行建立）
├── credentials.json       # Google API 憑證（需自行下載）
├── templates/
│   └── index.html         # 前端 UI
└── README.md              # 說明文件
```

## 注意事項

1. **資料表結構**：請根據實際需求調整 `models.py` 中的 `ActiveReward` 模型欄位
2. **欄位對應**：請根據實際 Google Sheets 的欄位名稱調整 `sync_service.py` 中的欄位對應
3. **唯一識別**：如果資料表需要避免重複，請在 `sync_service.py` 中加入唯一性檢查邏輯
4. **錯誤處理**：系統會記錄所有錯誤到日誌，請定期檢查日誌檔案

## 疑難排解

### 無法連接 Google Sheets

- 確認 `credentials.json` 檔案存在且格式正確
- 確認已啟用 Google Sheets API 和 Google Drive API
- 確認已將試算表分享給服務帳號的電子郵件

### 資料庫連接失敗

- 確認資料庫服務正在運行
- 檢查 `.env` 檔案中的資料庫連線資訊是否正確
- 確認資料庫使用者有足夠的權限

### 找不到確認欄位

- 確認試算表中存在包含「確認」或「confirmed」的欄位
- 檢查欄位名稱是否正確

## 授權

本專案僅供內部使用。

