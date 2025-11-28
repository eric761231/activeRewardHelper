# Netlify _redirects 檔案設定說明

## 重要：_redirects 檔案位置

`_redirects` 檔案**必須**放在 Netlify 的發布目錄中才能生效。

### 正確的檔案位置

```
netlify/
├── _redirects    ← 必須在這裡
├── index.html
└── favicon.svg
```

### 錯誤的檔案位置

```
_redirects        ← 這樣不會生效（在根目錄）
netlify/
├── index.html
└── favicon.svg
```

## 當前設定

`netlify/_redirects` 檔案包含以下代理規則：

```apache
# 後端 1：151.242.53.185
/api1/*  http://151.242.53.185:2998/api/:splat  200

# 後端 2：151.242.53.186
/api2/*  http://151.242.53.186:2998/api/:splat  200

# 後端 3：151.242.53.187
/api3/*  http://151.242.53.187:2998/api/:splat  200

# 後端 4：151.242.53.188
/api4/*  http://151.242.53.188:2998/api/:splat  200

# 後端 5：151.242.53.189（預設）
/api/*  http://151.242.53.189:2998/api/:splat  200
```

## 路徑匹配說明

當前端請求 `/api1/sync` 時：
- Netlify 匹配規則：`/api1/*`
- `:splat` 會匹配 `sync`
- 代理到：`http://151.242.53.185:2998/api/sync`

## 部署步驟

1. **確認檔案位置**：
   - 確保 `netlify/_redirects` 檔案存在
   - 檔案必須在 `netlify/` 目錄中

2. **推送到 GitHub**：
   ```bash
   git add netlify/_redirects
   git commit -m "新增 _redirects 檔案到 netlify 目錄"
   git push origin main
   ```

3. **Netlify 自動部署**：
   - Netlify 會自動偵測更改並重新部署
   - 部署完成後，`_redirects` 規則會生效

4. **驗證設定**：
   - 在 Netlify Dashboard 中檢查部署日誌
   - 確認 `_redirects` 檔案被包含在部署中

## 疑難排解

### 問題：仍然返回 404

**可能原因**：
1. `_redirects` 檔案不在 `netlify/` 目錄中
2. Netlify 還沒有重新部署
3. 檔案格式錯誤

**解決方法**：
1. 確認 `netlify/_redirects` 檔案存在
2. 在 Netlify Dashboard 中觸發手動重新部署
3. 檢查 Netlify 部署日誌，確認 `_redirects` 檔案被包含

### 問題：如何確認 _redirects 已生效

**方法 1：檢查 Netlify 部署日誌**
- 前往 Netlify Dashboard
- 查看最新的部署日誌
- 確認 `_redirects` 檔案被處理

**方法 2：測試代理**
- 在瀏覽器中打開：`https://your-site.netlify.app/api1/sync`
- 應該會代理到後端（可能會有 CORS 錯誤，但這表示代理正在工作）

## 手動觸發重新部署

如果自動部署沒有生效，可以：

1. **在 Netlify Dashboard**：
   - 前往您的網站
   - 點擊 "Deploys" 標籤
   - 點擊 "Trigger deploy" > "Clear cache and deploy site"

2. **使用 Netlify CLI**：
   ```bash
   netlify deploy --prod --dir=netlify
   ```

