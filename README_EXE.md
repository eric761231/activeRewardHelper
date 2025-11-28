# 建立獨立可執行檔案 (EXE)

## 說明

這個腳本會將 Python 應用程式打包成獨立的 EXE 檔案，不需要安裝 Python 或任何套件即可運行。

## 使用方式

### 方法 1：使用批次檔（推薦）

1. **雙擊執行 `build_exe.bat`**
   - 腳本會自動安裝 PyInstaller
   - 自動打包應用程式
   - 生成的 EXE 檔案在 `dist\activeRewardHelper.exe`

### 方法 2：手動執行

```bash
# 1. 安裝 PyInstaller
pip install pyinstaller

# 2. 打包應用程式
pyinstaller build_exe.spec

# 或使用簡化命令
pyinstaller --name=activeRewardHelper --onefile --add-data "config;config" app.py
```

## 打包後的檔案結構

```
dist/
└── activeRewardHelper.exe  # 可執行檔案

config/                     # 需要與 EXE 放在同一目錄
├── mysql_config.json
├── cloud_csv_config.json
└── keys/
    └── (Google 憑證檔案)
```

## 使用打包後的 EXE

1. **複製檔案**：
   - 將 `dist\activeRewardHelper.exe` 複製到您想要的目錄
   - 將 `config` 目錄也複製到相同位置

2. **設定檔案**：
   - 確保 `config\mysql_config.json` 已設定資料庫連線資訊
   - 確保 `config\cloud_csv_config.json` 已設定 Google Sheets 資訊
   - 確保 `config\keys\` 目錄中有 Google 憑證檔案

3. **執行**：
   - 雙擊 `activeRewardHelper.exe`
   - 應用程式會啟動在 `http://localhost:2999`

## 注意事項

1. **檔案大小**：
   - EXE 檔案會比較大（約 50-100 MB），因為包含了 Python 執行環境和所有套件

2. **首次啟動**：
   - 首次啟動可能需要幾秒鐘時間來解壓縮和載入

3. **防毒軟體**：
   - 某些防毒軟體可能會誤報，這是正常現象（PyInstaller 打包的檔案常見）

4. **設定檔位置**：
   - EXE 檔案需要與 `config` 目錄放在同一資料夾
   - 設定檔路徑是相對路徑

5. **日誌輸出**：
   - EXE 會顯示控制台視窗，方便查看日誌和錯誤訊息

## 疑難排解

### 問題：EXE 無法啟動

**解決方法**：
1. 確認 `config` 目錄存在且包含必要的設定檔
2. 檢查是否有錯誤訊息顯示在控制台視窗
3. 確認防火牆沒有阻擋應用程式

### 問題：找不到設定檔

**解決方法**：
1. 確認 `config` 目錄與 EXE 檔案在同一資料夾
2. 確認設定檔名稱正確（`mysql_config.json`、`cloud_csv_config.json`）

### 問題：EXE 檔案太大

**解決方法**：
1. 這是正常的，因為包含了完整的 Python 執行環境
2. 可以使用 UPX 壓縮（PyInstaller 會自動使用）

## 進階設定

如果需要自訂打包選項，可以編輯 `build_exe.spec` 檔案：

- `console=True/False`：是否顯示控制台視窗
- `onefile=True/False`：是否打包成單一檔案
- `upx=True/False`：是否使用 UPX 壓縮

