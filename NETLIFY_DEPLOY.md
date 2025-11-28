# Netlify 部署指南

## 重要說明

Netlify **無法直接運行 Flask 應用程式**。您需要採用以下架構：

- **前端（靜態檔案）**：部署到 Netlify
- **後端（Flask API）**：部署到其他平台（如 Render、Railway、Heroku）

## 部署步驟

### 第一步：部署後端 API

選擇以下其中一個平台部署 Flask 後端：

#### 選項 A：使用 Render（推薦，免費）

1. 前往 [Render](https://render.com/)
2. 註冊/登入帳號
3. 點擊 "New +" > "Web Service"
4. 連接您的 GitHub 儲存庫
5. 設定：
   - **Name**: `active-reward-api`（或您喜歡的名稱）
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

6. 在 Environment Variables 中設定：
   - 不需要設定，系統會從 `config/` 目錄讀取設定檔

7. 部署完成後，記下您的 API URL（例如：`https://active-reward-api.onrender.com`）

#### 選項 B：使用 Railway

1. 前往 [Railway](https://railway.app/)
2. 註冊/登入帳號
3. 點擊 "New Project" > "Deploy from GitHub repo"
4. 選擇您的儲存庫
5. Railway 會自動偵測 Python 專案
6. 在 Variables 中設定環境變數（如果需要）
7. 部署完成後，記下您的 API URL

### 第二步：更新 Netlify 設定

1. 編輯 `_redirects` 檔案，將後端 URL 替換為您實際的後端網址：

```apache
/api/*  https://your-backend-url.onrender.com/api/:splat  200
```

例如，如果後端部署在 Render：
```apache
/api/*  https://active-reward-api.onrender.com/api/:splat  200
```

### 第三步：部署前端到 Netlify

#### 方法 1：透過 Netlify Dashboard

1. 前往 [Netlify](https://app.netlify.com/)
2. 點擊 "Add new site" > "Import an existing project"
3. 連接您的 GitHub 儲存庫
4. 設定：
   - **Base directory**: 留空或設為專案根目錄
   - **Build command**: 留空（靜態網站不需要建置）
   - **Publish directory**: `netlify`

5. 點擊 "Deploy site"

#### 方法 2：使用 Netlify CLI

```bash
# 安裝 Netlify CLI
npm install -g netlify-cli

# 登入
netlify login

# 部署
netlify deploy --prod --dir=netlify
```

### 第四步：設定環境變數（可選）

如果您想要在前端直接指定後端 URL，可以在 Netlify 設定環境變數：

1. 前往 Netlify Dashboard > 您的網站 > Site settings > Environment variables
2. 新增變數：
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.onrender.com`

## 檔案結構說明

```
專案根目錄/
├── netlify/              # Netlify 部署目錄（前端靜態檔案）
│   ├── index.html        # 前端頁面
│   └── favicon.svg       # 網站圖示
├── templates/            # Flask 模板（開發用）
│   └── index.html
├── _redirects            # Netlify 重定向規則（API 代理）
├── netlify.toml          # Netlify 設定檔
├── app.py                # Flask 後端應用程式
└── ...其他檔案
```

## 測試部署

1. **測試前端**：訪問您的 Netlify URL（例如：`https://your-site.netlify.app`）
2. **測試 API**：點擊「開始發放」按鈕，確認能正常連接到後端

## 疑難排解

### 問題：API 請求失敗（CORS 錯誤）

**解決方案**：確保後端的 `app.py` 中有設定 CORS：

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": ["https://your-site.netlify.app"]}})
```

### 問題：找不到 API 端點

**解決方案**：
1. 檢查 `_redirects` 檔案中的後端 URL 是否正確
2. 確認後端已成功部署並運行
3. 檢查後端 URL 是否可訪問（在瀏覽器中打開後端 URL）

### 問題：前端找不到資源

**解決方案**：
1. 確認 `netlify/index.html` 中的資源路徑使用相對路徑
2. 確認 `favicon.svg` 等靜態資源在 `netlify/` 目錄中

## 注意事項

1. **免費方案限制**：
   - Render 免費方案在 15 分鐘無活動後會休眠，首次請求可能需要較長時間
   - 考慮使用 Railway 或其他平台，或升級到付費方案

2. **安全性**：
   - 不要在程式碼中硬編碼敏感資訊（如資料庫密碼）
   - 使用環境變數或設定檔管理敏感資訊

3. **資料庫連線**：
   - 確保資料庫允許從部署平台的 IP 連線
   - 檢查防火牆設定

## 快速檢查清單

- [ ] 後端已部署到 Render/Railway/Heroku
- [ ] 後端 URL 可正常訪問
- [ ] `_redirects` 檔案中的後端 URL 已更新
- [ ] 前端已部署到 Netlify
- [ ] CORS 設定正確
- [ ] 測試 API 連線正常

