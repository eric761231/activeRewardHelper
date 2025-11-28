# Google OAuth 2.0 redirect_uri 驗證規則（官方文件）

根據 [Google 官方文件](https://developers.google.com/identity/protocols/oauth2/web-server?hl=zh-tw#authorization-errors-redirect-uri-mismatch)，以下是 redirect_uri 的驗證規則：

## 官方驗證規則（必須完全匹配）

根據 Google 官方文件，redirect_uri 必須與 Google Cloud Console 中註冊的 URI **完全匹配**，包括：

1. **協議**（http 或 https）
2. **域名**（localhost、127.0.0.1 等）
3. **端口號**（如果有）
4. **路徑**（包括尾部斜線 '/'）
5. **大小寫**

**重要**：不能使用通配符，必須明確指定每個 URI。

## 桌面應用程式（Desktop Application）的 redirect_uri 規則

### 重要規則

1. **必須完全匹配**：
   - redirect_uri 必須與 Google Cloud Console 中註冊的 URI **完全一致**
   - 包括協議（http/https）、主機名、端口號、路徑

2. **localhost 的特殊處理**：
   - 對於桌面應用程式，Google 通常會自動允許 `http://localhost` 和 `http://127.0.0.1`
   - **但是**，如果使用了特定端口（如 `http://localhost:8080`），必須明確註冊

3. **端口號必須匹配**：
   - `http://localhost` ≠ `http://localhost:8080`
   - 如果應用程式使用 `http://localhost:8080`，必須在 Google Cloud Console 中註冊 `http://localhost:8080`

4. **路徑必須匹配**：
   - `http://localhost:8080` ≠ `http://localhost:8080/`
   - 結尾的斜線也會影響匹配

## 常見錯誤原因

### 錯誤 1：端口號不匹配

**情況**：
- Google Cloud Console 中只有：`http://localhost`
- 應用程式實際使用：`http://localhost:8080`

**解決方法**：
- 在 Google Cloud Console 中添加：`http://localhost:8080`

### 錯誤 2：路徑不匹配

**情況**：
- Google Cloud Console 中：`http://localhost:8080`
- 應用程式實際使用：`http://localhost:8080/`（有結尾斜線）

**解決方法**：
- 同時添加兩個版本：
  - `http://localhost:8080`
  - `http://localhost:8080/`

### 錯誤 3：協議不匹配

**情況**：
- Google Cloud Console 中：`https://localhost:8080`
- 應用程式實際使用：`http://localhost:8080`

**解決方法**：
- 確保協議一致（桌面應用程式通常使用 `http`）

## 最佳實踐

### 對於桌面應用程式

1. **添加多個常用 URI**：
   ```
   http://localhost
   http://localhost/
   http://localhost:8080
   http://localhost:8080/
   http://127.0.0.1
   http://127.0.0.1/
   http://127.0.0.1:8080
   http://127.0.0.1:8080/
   ```

2. **使用固定端口**：
   - 避免使用 `port=0`（自動選擇端口）
   - 使用固定端口（如 8080），並在 Google Cloud Console 中註冊

3. **檢查實際使用的 URI**：
   - 從應用程式日誌中查看實際使用的 redirect_uri
   - 確保該 URI 在 Google Cloud Console 中

## 驗證步驟

### 步驟 1：查看實際使用的 redirect_uri

1. 運行應用程式
2. 查看日誌中的授權 URL
3. 從 URL 中提取 `redirect_uri` 參數
4. URL 解碼後就是實際使用的 URI

例如：
```
https://accounts.google.com/o/oauth2/auth?redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F
```
解碼後：`http://localhost:8080/`

### 步驟 2：確認 Google Cloud Console 中有該 URI

1. 前往：https://console.cloud.google.com/apis/credentials
2. 找到您的 OAuth 客戶端
3. 檢查「授權的重定向 URI」列表
4. 確認實際使用的 URI 在列表中

### 步驟 3：如果不在列表中，添加它

1. 點擊「新增 URI」
2. 輸入實際使用的 URI（完全一致，包括端口號和路徑）
3. 點擊「儲存」
4. 等待 1-2 分鐘讓變更生效

## 官方文件參考

根據 [Google 官方文件](https://developers.google.com/identity/protocols/oauth2/web-server?hl=zh-tw#authorization-errors-redirect-uri-mismatch)：

> **redirect_uri_mismatch**：提供的 redirect_uri 與應用程式註冊的 redirect_uri 不匹配。

這表示：
- redirect_uri 必須**完全匹配**
- 不能使用通配符
- 必須明確指定每個 URI

## 針對您的問題

您已經添加了 `http://localhost` 和 `http://127.0.0.1`，但系統使用了帶端口號的 URI（如 `http://localhost:8080`）。

**解決方法**：
1. 在 Google Cloud Console 中添加包含端口號的 URI
2. 添加多個常用端口（8080, 8081, 8082 等）
3. 同時添加有斜線和無斜線的版本

## 完整 URI 列表（建議添加）

為了確保覆蓋所有情況，建議添加以下所有 URI：

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

這樣可以確保無論系統使用哪個端口，都能成功匹配。

