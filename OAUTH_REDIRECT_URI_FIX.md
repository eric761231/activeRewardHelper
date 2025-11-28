# OAuth 2.0 redirect_uri_mismatch 錯誤解決指南

## 錯誤說明

您遇到的錯誤：
```
錯誤 400：redirect_uri_mismatch
redirect_uri=http://localhost:62619/
```

這表示 Google Cloud Console 中設定的重定向 URI 與應用程式實際使用的 URI 不匹配。

## 快速解決方法

### 方法 1：在 Google Cloud Console 中添加 localhost URI（推薦）

1. **前往 Google Cloud Console**：
   - https://console.cloud.google.com/apis/credentials

2. **找到您的 OAuth 2.0 客戶端 ID**：
   - 左側選單 → 「API 和服務」→ 「憑證」
   - 找到「桌面應用程式」類型的客戶端 ID
   - 點擊客戶端名稱或編輯圖示

3. **添加授權的重定向 URI**：
   - 在「授權的重定向 URI」區段，點擊「新增 URI」
   - 添加以下 URI（一次添加一個）：
     ```
     http://localhost
     http://localhost:8080
     http://localhost:8081
     http://localhost:8082
     http://localhost:8083
     http://127.0.0.1
     http://127.0.0.1:8080
     http://127.0.0.1:8081
     http://127.0.0.1:8082
     http://127.0.0.1:8083
     ```
   - **重要**：對於桌面應用程式，Google 通常會自動允許 `http://localhost`，但建議明確添加常用端口

4. **儲存變更**：
   - 點擊「儲存」
   - 等待 1-2 分鐘讓變更生效

5. **重新運行應用程式**：
   - 刪除舊的 `token.json`（如果存在）：
     ```bash
     del config\keys\token.json
     ```
   - 重新啟動應用程式

### 方法 2：使用固定端口（更穩定）

如果方法 1 仍然失敗，可以修改代碼使用固定端口。

當前代碼已經設定為優先使用端口 8080，如果被占用會自動選擇其他端口。

**確保 Google Cloud Console 中有以下 URI**：
```
http://localhost:8080
http://localhost
```

## 為什麼會出現這個錯誤？

### 原因

當使用 `run_local_server(port=0)` 時，系統會自動選擇一個可用的端口（例如 62619）。但這個端口可能沒有在 Google Cloud Console 中註冊。

### 解決方案

1. **添加多個常用端口**：在 Google Cloud Console 中添加多個 localhost URI，覆蓋常用端口範圍
2. **使用固定端口**：修改代碼使用固定端口（如 8080），並在 Google Cloud Console 中註冊

## 詳細步驟（圖解）

### 步驟 1：打開 OAuth 客戶端設定

1. 前往：https://console.cloud.google.com/apis/credentials
2. 在「OAuth 2.0 客戶端 ID」區段，找到您的桌面應用程式客戶端
3. 點擊客戶端名稱或編輯圖示（鉛筆圖示）

### 步驟 2：添加重定向 URI

在「授權的重定向 URI」區段：

1. 點擊「新增 URI」按鈕
2. 輸入：`http://localhost`
3. 再次點擊「新增 URI」，輸入：`http://localhost:8080`
4. 繼續添加其他常用端口（8081, 8082 等）
5. 點擊「儲存」

### 步驟 3：驗證設定

1. 確認所有 URI 都已正確添加
2. 等待 1-2 分鐘讓變更生效
3. 重新運行應用程式

## 常見問題

### Q: 添加後仍然失敗？

**A: 可能的原因**：
1. 變更尚未生效（等待 5-10 分鐘）
2. 使用了不同的端口（檢查應用程式日誌）
3. 客戶端 ID 不正確（確認使用的是正確的客戶端）

**解決方法**：
1. 查看應用程式日誌，確認實際使用的 URI
2. 將該 URI 添加到 Google Cloud Console
3. 確認使用的是「桌面應用程式」類型的客戶端，不是「Web 應用程式」

### Q: 如何查看實際使用的 URI？

**A: 查看應用程式日誌**：
- 應用程式啟動時會顯示類似訊息：
  ```
  Please visit this URL to authorize this application: http://localhost:62619/...
  ```
- 將這個 URI 添加到 Google Cloud Console

### Q: 可以使用通配符嗎？

**A: 不可以**。Google OAuth 2.0 不支援通配符，必須明確指定每個 URI。

### Q: 為什麼需要添加多個端口？

**A: 因為**：
- `port=0` 會讓系統自動選擇可用端口
- 不同時間可能使用不同的端口
- 添加多個常用端口可以確保覆蓋大部分情況

## 快速修復清單

- [ ] 前往 Google Cloud Console → 憑證
- [ ] 找到桌面應用程式 OAuth 客戶端
- [ ] 添加 `http://localhost`
- [ ] 添加 `http://localhost:8080`
- [ ] 添加 `http://127.0.0.1`
- [ ] 添加 `http://127.0.0.1:8080`
- [ ] 點擊「儲存」
- [ ] 等待 1-2 分鐘
- [ ] 刪除 `config/keys/token.json`
- [ ] 重新運行應用程式

## 驗證修復

修復後，重新運行應用程式：

1. **刪除舊令牌**：
   ```bash
   del config\keys\token.json
   ```

2. **重新啟動**：
   ```bash
   python app.py
   ```

3. **應該會成功**：
   - 瀏覽器會自動打開
   - 可以正常登入和授權
   - 不再出現 `redirect_uri_mismatch` 錯誤

## 預防措施

為了避免未來出現此問題：

1. **使用固定端口**：代碼已經設定為優先使用 8080
2. **預先添加常用 URI**：在 Google Cloud Console 中添加多個 localhost URI
3. **記錄實際 URI**：在日誌中記錄實際使用的 URI，以便除錯

