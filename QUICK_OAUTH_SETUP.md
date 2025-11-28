# OAuth 2.0 快速設定指南

## 快速開始

### 1. 下載 OAuth 2.0 憑證

1. 前往：https://console.cloud.google.com/
2. 選擇專案（或建立新專案）
3. 啟用「Google Sheets API」
4. 建立 OAuth 2.0 客戶端 ID：
   - 類型：**桌面應用程式**
   - 下載 JSON 檔案
5. 將下載的檔案重新命名為 `client_secrets.json`
6. 放到 `config/keys/` 目錄

### 2. 更新設定檔

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

### 3. 第一次運行

1. 啟動後端：
   ```bash
   python app.py
   ```

2. 第一次運行時：
   - 瀏覽器會自動打開
   - 登入您的 Google 帳號
   - 點擊「允許」授權
   - 完成後關閉瀏覽器

3. 之後的運行：
   - 不需要再次授權
   - 系統會自動使用儲存的令牌

## 檔案位置

```
config/
└── keys/
    ├── client_secrets.json    ← 從 Google Cloud Console 下載
    └── token.json             ← 系統自動建立（第一次授權後）
```

## 詳細說明

完整的設定說明請參考：`OAUTH_SETUP.md`

