# 簡單部署方案

## 架構說明

- **後端**：在本地運行（使用 `start_backend.bat` 啟動）
- **前端**：部署到 Netlify（靜態 HTML 頁面）

## 使用步驟

### 1. 啟動後端（必須先執行）

雙擊執行 `start_backend.bat`，後端會運行在 `http://localhost:5000`

**重要**：保持此視窗開啟，不要關閉！

### 2. 使用前端

#### 方案 A：本地測試
直接在瀏覽器打開 `netlify/index.html` 或使用 Live Server

#### 方案 B：部署到 Netlify
1. 將 `netlify/` 目錄部署到 Netlify
2. 在 Netlify 上設定環境變數 `API_BASE_URL` 為您的後端 URL
   - 如果後端在本地：無法直接訪問（需要使用 ngrok）
   - 如果後端已部署：使用後端的公開 URL

## 本地開發流程

1. **啟動後端**：
   ```bash
   # 雙擊 start_backend.bat
   # 或
   python app.py
   ```

2. **打開前端**：
   - 直接用瀏覽器打開 `netlify/index.html`
   - 或使用 Live Server 在 `http://localhost:5500` 打開

3. **使用系統**：
   - 前端會自動連接到 `http://localhost:5000` 的後端
   - 點擊「開始發放」按鈕即可

## 如果需要讓 Netlify 前端訪問本地後端

需要使用 **ngrok** 將本地後端暴露到公網：

1. 下載並安裝 [ngrok](https://ngrok.com/)
2. 啟動後端（`start_backend.bat`）
3. 在另一個終端執行：
   ```bash
   ngrok http 5000
   ```
4. 複製 ngrok 提供的 URL（例如：`https://abcd1234.ngrok.io`）
5. 在 Netlify 環境變數中設定：
   - `API_BASE_URL` = `https://abcd1234.ngrok.io`

## 檔案說明

- `start_backend.bat` - 啟動後端服務（Windows）
- `netlify/index.html` - 前端頁面（可部署到 Netlify）
- `app.py` - Flask 後端應用程式

## 注意事項

1. **後端必須先啟動**：前端無法在後端未啟動時工作
2. **CORS 設定**：後端已設定允許跨域請求
3. **本地測試**：前端和後端都在本地時，會自動使用 `http://localhost:5000`

