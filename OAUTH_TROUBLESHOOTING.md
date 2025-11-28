# OAuth 2.0 授權問題詳細診斷

## 問題：已添加 localhost URI 但仍出現 redirect_uri_mismatch

如果您已經在 Google Cloud Console 中添加了 `http://localhost` 和 `http://127.0.0.1`，但仍然出現錯誤，請按照以下步驟診斷：

## 診斷步驟

### 步驟 1：確認 OAuth 客戶端類型

**重要**：必須是「**桌面應用程式**」類型，不是「Web 應用程式」！

1. 前往：https://console.cloud.google.com/apis/credentials
2. 找到您的 OAuth 客戶端
3. **確認應用程式類型**：
   - ✅ 應該是「桌面應用程式」
   - ❌ 不應該是「Web 應用程式」

如果類型錯誤：
- 建立新的「桌面應用程式」OAuth 客戶端
- 下載新的憑證檔案
- 更新 `config/cloud_csv_config.json` 中的路徑

### 步驟 2：檢查實際使用的 URI

從日誌中查看實際使用的 URI：

1. **查看應用程式日誌**，找到類似這樣的訊息：
   ```
   Please visit this URL to authorize this application: 
   https://accounts.google.com/o/oauth2/auth?redirect_uri=http%3A%2F%2Flocalhost%3A62739%2F
   ```

2. **提取 redirect_uri**：
   - 從 URL 中找出 `redirect_uri=` 後面的值
   - 例如：`http://localhost:62739/`（需要 URL 解碼）

3. **確認該 URI 是否在 Google Cloud Console 中**：
   - 如果日誌顯示 `http://localhost:62739/`
   - 需要在 Google Cloud Console 中添加：`http://localhost:62739`

### 步驟 3：確認 URI 格式完全一致

**重要**：URI 必須完全匹配，包括：
- 協議（http vs https）
- 主機名（localhost vs 127.0.0.1）
- 端口號（如果有）
- 路徑（結尾的 `/`）

**常見錯誤**：
- ❌ 添加了 `http://localhost` 但實際使用 `http://localhost:8080`
- ❌ 添加了 `http://localhost:8080` 但實際使用 `http://localhost:8080/`（結尾有斜線）
- ❌ 添加了 `http://localhost` 但實際使用 `https://localhost`（協議不同）

### 步驟 4：檢查憑證檔案

1. **確認憑證檔案路徑正確**：
   - 檢查 `config/cloud_csv_config.json` 中的 `credentials_file`
   - 確認檔案確實存在於該路徑

2. **檢查憑證檔案內容**：
   - 打開 `config/keys/client_secrets.json`
   - 確認 `installed.client_id` 與 Google Cloud Console 中的客戶端 ID 一致
   - 確認是「桌面應用程式」類型的憑證

### 步驟 5：等待變更生效

Google Cloud Console 的變更可能需要時間生效：
- **通常**：1-2 分鐘
- **最長**：5-10 分鐘

**建議**：
1. 添加 URI 後，等待 5 分鐘
2. 清除瀏覽器快取
3. 重新運行應用程式

### 步驟 6：檢查 OAuth 同意畫面

1. 前往：https://console.cloud.google.com/apis/credentials/consent
2. 確認 OAuth 同意畫面已設定完成
3. 如果應用程式在「測試」模式：
   - 在「測試使用者」中添加您的 Google 帳號
   - 或將應用程式發布為「生產」模式

## 快速修復清單

按照以下順序檢查：

- [ ] **確認 OAuth 客戶端類型是「桌面應用程式」**
- [ ] **查看日誌，確認實際使用的 redirect_uri**
- [ ] **在 Google Cloud Console 中添加該 URI（包括端口號）**
- [ ] **確認 URI 格式完全一致（包括結尾的斜線）**
- [ ] **等待 5 分鐘讓變更生效**
- [ ] **清除瀏覽器快取**
- [ ] **刪除 `config/keys/token.json`**
- [ ] **重新運行應用程式**

## 如果仍然失敗

### 方法 1：添加所有可能的 URI

在 Google Cloud Console 中，添加以下所有 URI：

```
http://localhost
http://localhost/
http://localhost:8080
http://localhost:8080/
http://localhost:8081
http://localhost:8081/
http://localhost:8082
http://localhost:8082/
http://localhost:8083
http://localhost:8083/
http://localhost:8084
http://localhost:8084/
http://127.0.0.1
http://127.0.0.1/
http://127.0.0.1:8080
http://127.0.0.1:8080/
```

### 方法 2：使用固定端口並確保可用

1. **檢查端口 8080 是否被占用**：
   ```bash
   netstat -ano | findstr :8080
   ```

2. **如果被占用，關閉該程式**：
   - 找到 PID
   - 在任務管理器中結束進程

3. **重新運行應用程式**：
   - 應該會使用端口 8080
   - 確保 Google Cloud Console 中有 `http://localhost:8080`

### 方法 3：查看詳細日誌

在 `sheets_service.py` 中添加更詳細的日誌：

```python
logger.info(f"嘗試使用的 redirect_uri: {redirect_uri}")
logger.info(f"OAuth 客戶端 ID: {client_id}")
```

然後查看日誌，確認實際使用的 URI。

## 常見問題

### Q: 為什麼添加了 `http://localhost` 還是不行？

**A: 可能的原因**：
1. 系統使用了特定端口（如 8080），需要明確添加 `http://localhost:8080`
2. URI 格式不完全一致（結尾斜線、大小寫等）
3. 變更尚未生效（需要等待）

**解決方法**：
- 查看日誌確認實際使用的 URI
- 添加包含端口號的完整 URI

### Q: 如何查看實際使用的 redirect_uri？

**A: 方法**：
1. 查看應用程式日誌中的授權 URL
2. 從 URL 中提取 `redirect_uri` 參數
3. URL 解碼後就是實際使用的 URI

例如：
```
https://accounts.google.com/o/oauth2/auth?redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F
```
解碼後：`http://localhost:8080/`

### Q: 桌面應用程式和 Web 應用程式有什麼區別？

**A: 區別**：
- **桌面應用程式**：使用 `InstalledAppFlow`，重定向到 `localhost`
- **Web 應用程式**：使用 `Flow`，重定向到 Web URL

**如果類型錯誤**：
- 會導致 `redirect_uri_mismatch` 錯誤
- 需要建立正確類型的客戶端

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
   - 瀏覽器自動打開
   - 可以正常登入和授權
   - 不再出現 `redirect_uri_mismatch` 錯誤

