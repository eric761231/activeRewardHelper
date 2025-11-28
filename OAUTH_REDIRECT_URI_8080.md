# OAuth 2.0 重定向 URI 設定（端口 8080）

## 問題
當端口從 2998 改為 8080 後，Google Cloud Console 中的重定向 URI 需要更新。

## 解決方法

### 步驟 1：前往 Google Cloud Console
1. 打開 [Google Cloud Console](https://console.cloud.google.com/)
2. 選擇您的專案
3. 前往「API 和服務」→「憑證」
4. 找到您的 OAuth 2.0 客戶端 ID（桌面應用程式或網頁應用程式）
5. 點擊編輯（鉛筆圖示）

### 步驟 2：添加重定向 URI

根據您的 OAuth 客戶端類型，添加以下 URI：

#### 如果是「桌面應用程式」類型：
在「已授權的重新導向 URI」中添加：
```
http://localhost:8080/
http://localhost:8080
http://localhost:8081/
http://localhost:8081
http://localhost:8082/
http://localhost:8082
http://localhost:8083/
http://localhost:8083
http://localhost:8084/
http://localhost:8084
http://127.0.0.1:8080/
http://127.0.0.1:8080
http://127.0.0.1:8081/
http://127.0.0.1:8081
http://127.0.0.1:8082/
http://127.0.0.1:8082
http://127.0.0.1:8083/
http://127.0.0.1:8083
http://127.0.0.1:8084/
http://127.0.0.1:8084
```

#### 如果是「網頁應用程式」類型：
在「已授權的 JavaScript 來源」中添加：
```
http://localhost
http://localhost:8080
http://127.0.0.1
http://127.0.0.1:8080
```

在「已授權的重新導向 URI」中添加：
```
http://localhost:8080/
http://localhost:8080
http://localhost:8081/
http://localhost:8081
http://localhost:8082/
http://localhost:8082
http://localhost:8083/
http://localhost:8083
http://localhost:8084/
http://localhost:8084
http://127.0.0.1:8080/
http://127.0.0.1:8080
http://127.0.0.1:8081/
http://127.0.0.1:8081
http://127.0.0.1:8082/
http://127.0.0.1:8082
http://127.0.0.1:8083/
http://127.0.0.1:8083
http://127.0.0.1:8084/
http://127.0.0.1:8084
```

### 步驟 3：儲存設定
點擊「儲存」按鈕

### 步驟 4：重新測試
1. 刪除舊的令牌檔案（如果存在）：
   ```bash
   del config\keys\token.json
   ```

2. 重新啟動應用程式：
   ```bash
   python app.py
   ```

3. 觸發同步功能，應該會自動打開瀏覽器進行 OAuth 授權

## 注意事項
- 確保添加的 URI 與代碼中使用的端口一致（8080-8084）
- 注意 URI 的格式：有些需要尾隨斜線 `/`，有些不需要
- 如果仍然出現錯誤，請檢查瀏覽器地址欄中的實際重定向 URI，並確保該 URI 已在 Google Cloud Console 中註冊

