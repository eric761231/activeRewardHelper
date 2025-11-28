# 服務帳號 vs 個人 Google 帳號

## 為什麼使用服務帳號？

### 服務帳號的優點

1. **自動化友好**
   - ✅ 不需要用戶登入或授權
   - ✅ 適合後端服務和自動化腳本
   - ✅ 可以 24/7 運行，無需人工干預

2. **安全性**
   - ✅ 權限範圍明確（只訪問指定的 Sheet）
   - ✅ 可以隨時撤銷，不影響個人帳號
   - ✅ 不會暴露個人帳號的密碼或完整權限

3. **穩定性**
   - ✅ 令牌不會過期（或過期時間很長）
   - ✅ 不需要定期重新授權
   - ✅ 適合生產環境

4. **多用戶共享**
   - ✅ 多個系統可以共用同一個服務帳號
   - ✅ 不依賴特定人員的個人帳號

### 個人 Google 帳號的限制

1. **需要用戶授權**
   - ❌ 第一次使用需要用戶登入並授權（OAuth 流程）
   - ❌ 如果用戶撤銷權限，系統會中斷

2. **令牌管理複雜**
   - ❌ 訪問令牌（access token）會過期（通常 1 小時）
   - ❌ 需要刷新令牌（refresh token）來獲取新的訪問令牌
   - ❌ 需要處理令牌過期的情況

3. **依賴個人帳號**
   - ❌ 如果個人帳號被停用或刪除，系統會中斷
   - ❌ 如果員工離職，需要轉移權限

4. **安全性考量**
   - ❌ 需要儲存刷新令牌（敏感資訊）
   - ❌ 如果個人帳號被盜用，影響更大

## 技術實現差異

### 服務帳號（當前實現）

```python
# 使用服務帳號憑證檔案
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://spreadsheets.google.com/feeds']
)
client = gspread.authorize(creds)
```

**優點**：
- 簡單直接
- 不需要用戶交互
- 一次設定，長期使用

### 個人 Google 帳號（OAuth 2.0）

```python
# 需要 OAuth 2.0 流程
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 1. 第一次：用戶需要登入並授權
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://spreadsheets.google.com/feeds']
)
creds = flow.run_local_server()

# 2. 儲存刷新令牌
with open('token.json', 'w') as token:
    token.write(creds.to_json())

# 3. 後續使用：需要檢查令牌是否過期並刷新
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
```

**缺點**：
- 需要用戶第一次授權
- 需要處理令牌過期
- 需要儲存和管理刷新令牌

## 如果要用個人 Google 帳號

### 需要做的改變

1. **建立 OAuth 2.0 憑證**
   - 在 Google Cloud Console 建立 OAuth 2.0 客戶端 ID
   - 下載 `client_secrets.json`

2. **修改認證流程**
   - 第一次運行時，需要用戶在瀏覽器中登入並授權
   - 儲存刷新令牌到 `token.json`

3. **處理令牌刷新**
   - 每次使用前檢查令牌是否過期
   - 如果過期，使用刷新令牌獲取新的訪問令牌

4. **更新代碼**
   - 修改 `sheets_service.py` 中的認證邏輯
   - 添加令牌管理功能

### 範例代碼結構

```python
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://spreadsheets.google.com/feeds']

def get_credentials():
    creds = None
    # 檢查是否已有儲存的令牌
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 如果沒有憑證或憑證已過期
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 刷新令牌
            creds.refresh(Request())
        else:
            # 第一次使用，需要用戶授權
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 儲存憑證供下次使用
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds
```

## 建議

### 使用服務帳號的情況（推薦）

- ✅ 後端服務/自動化系統
- ✅ 不需要用戶交互
- ✅ 需要 24/7 運行
- ✅ 多個系統共用
- ✅ 生產環境

### 使用個人帳號的情況

- ✅ 前端應用（用戶自己的資料）
- ✅ 需要訪問用戶的個人資料
- ✅ 臨時腳本或一次性任務
- ✅ 開發/測試環境

## 當前系統的建議

**建議繼續使用服務帳號**，因為：

1. 這是後端服務，需要自動化運行
2. 不需要用戶登入
3. 更穩定可靠
4. 只需要一次設定（分享 Sheet 給服務帳號）

**如果確實需要使用個人帳號**，我可以幫您：
1. 修改代碼以支援 OAuth 2.0
2. 添加令牌管理功能
3. 處理第一次授權流程

但這會讓系統變得更複雜，且需要用戶第一次運行時進行授權。

