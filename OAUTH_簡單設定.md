# OAuth 2.0 簡單設定指南（端口 8080）

## 問題
OAuth 授權一直失敗，出現 `redirect_uri_mismatch` 錯誤。

## 最簡單的解決方法

### 步驟 1：確保端口 8080 可用
檢查端口是否被占用：
```powershell
netstat -ano | findstr :8080
```
如果有程序占用，請關閉它。

### 步驟 2：在 Google Cloud Console 設定

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 選擇您的專案
3. 前往「API 和服務」→「憑證」
4. 找到您的 OAuth 2.0 客戶端 ID（**網頁應用程式**類型）
5. 點擊編輯（鉛筆圖示）

### 步驟 3：只添加這 4 個 URI（最簡單）

#### 在「已授權的 JavaScript 來源」中添加：
```
http://localhost
http://localhost:8080
http://127.0.0.1
http://127.0.0.1:8080
```

#### 在「已授權的重新導向 URI」中添加：
```
http://localhost:8080/
http://localhost:8080
http://127.0.0.1:8080/
http://127.0.0.1:8080
```

**重要：**
- 必須包含帶斜線 `/` 和不帶斜線的版本
- 只添加這 4 個，不要添加其他端口
- 確保格式完全一致（沒有多餘的空格）

### 步驟 4：儲存並測試

1. 點擊「儲存」按鈕
2. **等待 1-2 分鐘**（Google 需要時間更新設定）
3. 刪除舊的令牌檔案：
   ```powershell
   del config\keys\token.json
   ```
4. 重新啟動應用程式：
   ```powershell
   python app.py
   ```
5. 觸發同步功能

## 如果還是不行

### 檢查實際使用的 URI
當出現錯誤時，查看瀏覽器地址欄中的完整 URL，找到 `redirect_uri=` 後面的值，那就是實際使用的 URI。

例如：
```
redirect_uri=http://localhost:8080/
```

確保這個**完全相同的 URI**（包括斜線）已經在 Google Cloud Console 中。

### 常見問題

1. **端口被占用**
   - 解決：關閉占用端口 8080 的程式

2. **URI 格式不一致**
   - 解決：確保 Google Cloud Console 中的 URI 與實際使用的完全一致（包括斜線）

3. **設定未生效**
   - 解決：等待 1-2 分鐘後再試

4. **使用了錯誤的客戶端類型**
   - 解決：確保使用的是「網頁應用程式」類型的客戶端 ID

