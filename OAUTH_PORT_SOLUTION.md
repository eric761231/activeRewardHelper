# OAuth 2.0 端口問題解決方案

## 問題說明

從日誌中可以看到，系統使用了不同的自動選擇端口：
- `http://localhost:62739/`
- `http://localhost:62748/`
- `http://localhost:62752/`

這表示端口 8080 被占用，系統自動選擇了其他可用端口。但這些端口可能沒有在 Google Cloud Console 中註冊。

## 解決方案

### 方案 1：添加所有可能的端口（不推薦）

在 Google Cloud Console 中添加大量端口是不切實際的，因為端口範圍很大。

### 方案 2：確保端口 8080 可用（推薦）

1. **檢查端口 8080 是否被占用**：
   ```bash
   # Windows PowerShell
   netstat -ano | findstr :8080
   ```

2. **如果被占用，關閉占用端口的程式**：
   - 找到占用端口的 PID
   - 在任務管理器中結束該進程

3. **重新運行應用程式**：
   - 系統會使用端口 8080
   - 確保 Google Cloud Console 中有 `http://localhost:8080`

### 方案 3：使用更廣泛的 localhost URI（最簡單）

Google 對於桌面應用程式，通常會自動允許 `http://localhost`（不指定端口）。

在 Google Cloud Console 中，確保有以下 URI：
```
http://localhost
http://127.0.0.1
```

**注意**：某些版本的 Google OAuth 可能要求明確指定端口。

### 方案 4：修改代碼使用固定端口範圍

如果 8080 經常被占用，可以修改代碼嘗試多個固定端口：

```python
# 嘗試多個固定端口
for port in [8080, 8081, 8082, 8083, 8084]:
    try:
        creds = flow.run_local_server(port=port)
        break
    except OSError:
        continue
else:
    # 如果所有端口都被占用，使用自動選擇
    creds = flow.run_local_server(port=0)
```

然後在 Google Cloud Console 中註冊這些端口。

## 立即解決步驟

### 步驟 1：檢查端口 8080

```bash
# Windows PowerShell
netstat -ano | findstr :8080
```

如果沒有輸出，表示端口 8080 可用。

### 步驟 2：在 Google Cloud Console 中添加 URI

1. 前往：https://console.cloud.google.com/apis/credentials
2. 找到您的桌面應用程式 OAuth 客戶端
3. 確保有以下 URI：
   ```
   http://localhost
   http://localhost:8080
   http://127.0.0.1
   http://127.0.0.1:8080
   ```

### 步驟 3：關閉占用端口的程式

如果端口 8080 被占用：
1. 找到占用端口的 PID（從 netstat 輸出）
2. 在任務管理器中結束該進程
3. 或使用命令：
   ```bash
   taskkill /PID <PID號碼> /F
   ```

### 步驟 4：重新運行應用程式

1. 刪除舊的令牌：
   ```bash
   del config\keys\token.json
   ```

2. 重新啟動應用程式：
   ```bash
   python app.py
   ```

3. 應該會使用端口 8080，授權應該會成功

## 為什麼會使用不同端口？

當使用 `run_local_server(port=0)` 時：
- 系統會自動選擇一個可用的端口
- 每次運行可能選擇不同的端口
- 這導致需要在 Google Cloud Console 中註冊多個 URI

## 最佳實踐

1. **使用固定端口**：確保端口 8080 可用
2. **添加常用 URI**：在 Google Cloud Console 中添加 `http://localhost` 和 `http://localhost:8080`
3. **檢查端口占用**：啟動應用程式前檢查端口是否可用

## 驗證

修復後，重新運行應用程式，日誌應該顯示：
```
正在啟動 OAuth 2.0 授權流程（桌面應用程式）...
瀏覽器將自動打開，請登入您的 Google 帳號並授權
```

授權 URL 應該使用 `http://localhost:8080`，而不是隨機端口。

