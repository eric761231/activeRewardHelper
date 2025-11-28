# IDE 設定指南

如果您的 IDE（如 VS Code、PyCharm 等）顯示 `ModuleNotFoundError`，但命令列可以正常運行，請按照以下步驟設定：

## VS Code 設定

### 1. 選擇正確的 Python 解釋器

1. 按 `Ctrl+Shift+P` 開啟命令面板
2. 輸入 `Python: Select Interpreter`
3. 選擇：`C:\Users\eric7\AppData\Local\Programs\Python\Python313\python.exe`

### 2. 重新載入視窗

1. 按 `Ctrl+Shift+P`
2. 輸入 `Developer: Reload Window`
3. 重新載入視窗

### 3. 檢查 Python 路徑設定

在 VS Code 設定中（`settings.json`）加入：

```json
{
    "python.defaultInterpreterPath": "C:\\Users\\eric7\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
    "python.terminal.activateEnvironment": true
}
```

## PyCharm 設定

### 1. 設定專案解釋器

1. 前往 `File` > `Settings` > `Project` > `Python Interpreter`
2. 點擊齒輪圖示 > `Add...`
3. 選擇 `System Interpreter`
4. 選擇：`C:\Users\eric7\AppData\Local\Programs\Python\Python313\python.exe`
5. 點擊 `OK`

### 2. 重新索引專案

1. 前往 `File` > `Invalidate Caches...`
2. 選擇 `Invalidate and Restart`

## 驗證設定

執行以下命令確認 IDE 使用的 Python 解釋器：

```python
import sys
print(sys.executable)
```

應該顯示：`C:\Users\eric7\AppData\Local\Programs\Python\Python313\python.exe`

## 如果問題仍然存在

1. **重新安裝套件到正確的環境**：
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **檢查 IDE 的終端是否使用正確的 Python**：
   ```bash
   python --version
   python -m pip list | findstr flask
   ```

3. **使用命令列執行**（如果 IDE 仍有問題）：
   ```bash
   python app.py
   ```

## 快速診斷

執行環境檢查腳本：

```bash
python check_environment.py
```

這會顯示：
- Python 版本和路徑
- 已安裝的套件
- 模組導入測試結果

