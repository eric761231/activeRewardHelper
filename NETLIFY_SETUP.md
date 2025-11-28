# Netlify 部署設定說明

## 概述

本專案的前端部署在 Netlify，後端運行在獨立的伺服器上。Netlify 透過 `_redirects` 檔案將 API 請求代理到後端伺服器，避免混合內容（Mixed Content）問題。

## 檔案結構

```
netlify/
├── _redirects      # Netlify 代理規則
├── index.html      # 前端頁面
└── favicon.svg     # 網站圖示
```

## _redirects 檔案設定

### 重要：檔案位置

`_redirects` 檔案**必須**放在 `netlify/` 目錄中才能生效。

### 多後端故障轉移設定

系統支援多個後端 IP 的故障轉移功能，透過不同的路徑實現：

```
/api1/*  → http://151.242.53.185:2998/api/:splat
/api2/*  → http://151.242.53.186:2998/api/:splat
/api3/*  → http://151.242.53.187:2998/api/:splat
/api4/*  → http://151.242.53.188:2998/api/:splat
/api/*   → http://151.242.53.189:2998/api/:splat  (預設)
```

### 故障轉移流程

前端會按順序嘗試以下路徑：
1. `/api1/sync` → 後端 1 (151.242.53.185)
2. `/api2/sync` → 後端 2 (151.242.53.186)
3. `/api3/sync` → 後端 3 (151.242.53.187)
4. `/api4/sync` → 後端 4 (151.242.53.188)
5. `/api/sync` → 後端 5 (151.242.53.189) - 預設

如果某個後端無法連接，會自動嘗試下一個。

## 部署步驟

### 1. 確認檔案位置

確保 `_redirects` 檔案在 `netlify/` 目錄中：
```
netlify/_redirects  ✅ 正確
_redirects          ❌ 錯誤（不會生效）
```

### 2. 推送到 GitHub

```bash
git add netlify/_redirects
git commit -m "更新 Netlify 代理規則"
git push origin main
```

### 3. Netlify 自動部署

- Netlify 會自動偵測更改並重新部署
- 部署完成後，`_redirects` 規則會生效

### 4. 手動觸發重新部署（如果需要）

1. 前往 Netlify Dashboard：https://app.netlify.com/
2. 選擇您的網站
3. 點擊 "Deploys" 標籤
4. 點擊 "Trigger deploy" > "Clear cache and deploy site"

## 路徑匹配說明

當前端請求 `/api1/sync` 時：
- Netlify 匹配規則：`/api1/*`
- `:splat` 會匹配 `sync`
- 代理到：`http://151.242.53.185:2998/api/sync`

## 驗證設定

### 方法 1：檢查 Netlify 部署日誌

- 前往 Netlify Dashboard
- 查看最新的部署日誌
- 確認 `_redirects` 檔案被處理

### 方法 2：測試代理

在瀏覽器中打開：
```
https://your-site.netlify.app/api1/sync
```

應該會代理到後端（可能會有 CORS 或連接錯誤，但這表示代理正在工作）。

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

### 問題：混合內容錯誤

如果前端是 HTTPS，後端是 HTTP，會出現混合內容錯誤。解決方法：
- 使用 Netlify 的代理功能（透過 `_redirects`）
- 或將後端升級為 HTTPS

## 相關檔案

- `netlify/_redirects` - Netlify 代理規則
- `netlify/index.html` - 前端頁面（包含故障轉移邏輯）
- `netlify.toml` - Netlify 配置檔案

