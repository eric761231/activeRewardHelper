# OAuth 2.0 redirect_uri_mismatch 錯誤解決指南

## 錯誤說明

`redirect_uri_mismatch` 錯誤表示 Google Cloud Console 中設定的重定向 URI 與應用程式實際使用的 URI 不匹配。

## 錯誤原因

當使用 `run_local_server(port=0)` 時，系統會自動選擇一個可用的端口（例如：`http://localhost:8080`），但這個 URI 可能沒有在 Google Cloud Console 中註冊。

## 解決方法

### 方法 1：在 Google Cloud Console 中添加重定向 URI（推薦）

1. **前往 Google Cloud Console**：
   - https://console.cloud.google.com/

2. **導航到 OAuth 客戶端設定**：
   - 左側選單 → 「API 和服務」→ 「憑證」
   - 找到您的 OAuth 2.0 客戶端 ID（桌面應用程式）
   - 點擊客戶端 ID 名稱或編輯圖示

3. **添加授權的重定向 URI**：
   - 在「授權的重定向 URI」區段，點擊「新增 URI」
   - 添加以下 URI（根據您的需求選擇）：
     ```
     http://localhost
     http://localhost:8080
     http://localhost:8081
     http://localhost:8082
     http://127.0.0.1
     http://127.0.0.1:8080
     http://127.0.0.1:8081
     http://127.0.0.1:8082
     ```
   - **注意**：對於桌面應用程式，Google 通常會自動允許 `http://localhost` 和 `http://127.0.0.1`，但建議明確添加常用的端口

4. **儲存變更**：
   - 點擊「儲存」

5. **等待生效**：
   - 變更可能需要幾分鐘才能生效
   - 如果仍然失敗，請等待 5-10 分鐘後重試

### 方法 2：使用固定的端口號（更穩定）

修改 `sheets_service.py`，使用固定的端口號：

```python
# 在 _authorize 方法中，將：
creds = flow.run_local_server(port=0)

# 改為：
creds = flow.run_local_server(port=8080)
```

然後在 Google Cloud Console 中添加：
```
http://localhost:8080
```

### 方法 3：使用 OOB（Out-of-Band）流程（不推薦，已棄用）

Google 已棄用 OOB 流程，不建議使用。

## 詳細步驟（圖解）

### 步驟 1：找到 OAuth 客戶端設定

1. 前往：https://console.cloud.google.com/apis/credentials
2. 在「OAuth 2.0 客戶端 ID」區段，找到您的桌面應用程式客戶端
3. 點擊客戶端名稱或編輯圖示

### 步驟 2：添加重定向 URI

在「授權的重定向 URI」區段：

1. 點擊「新增 URI」按鈕
2. 輸入：`http://localhost`
3. 再次點擊「新增 URI」，輸入：`http://localhost:8080`
4. 可以繼續添加其他常用端口：`8081`, `8082` 等
5. 點擊「儲存」

### 步驟 3：驗證設定

1. 確認 URI 已正確添加
2. 等待幾分鐘讓變更生效
3. 重新運行應用程式

## 常見問題

### Q: 為什麼需要添加多個 URI？

A: 因為 `port=0` 會讓系統自動選擇可用端口，可能使用不同的端口號。添加多個常用端口可以確保覆蓋大部分情況。

### Q: 可以使用通配符嗎？

A: 不可以。Google OAuth 2.0 不支援通配符，必須明確指定每個 URI。

### Q: 添加後仍然失敗？

A: 可能的原因：
1. 變更尚未生效（等待 5-10 分鐘）
2. 使用了不同的 URI（檢查應用程式日誌中的實際 URI）
3. 客戶端 ID 不正確（確認使用的是正確的客戶端 ID）

### Q: 如何查看實際使用的 URI？

A: 查看應用程式日誌，應該會顯示類似以下訊息：
```
Please visit this URL to authorize this application: http://localhost:8080/...
```

將這個 URI 添加到 Google Cloud Console 中。

## 快速修復腳本

如果您想快速添加多個常用 URI，可以：

1. 在 Google Cloud Console 中，一次添加以下所有 URI：
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

2. 這樣可以覆蓋大部分自動選擇的端口

## 驗證修復

修復後，重新運行應用程式：

1. 刪除舊的 `token.json`（如果存在）：
   ```bash
   del config\keys\token.json
   ```

2. 重新啟動應用程式：
   ```bash
   python app.py
   ```

3. 應該會成功打開授權頁面，不再出現 `redirect_uri_mismatch` 錯誤

## 預防措施

為了避免未來出現此問題，建議：

1. **使用固定端口**：修改代碼使用固定端口（如 8080）
2. **在 Google Cloud Console 中預先添加常用 URI**
3. **記錄實際使用的 URI**：在日誌中記錄實際使用的 URI，以便除錯

