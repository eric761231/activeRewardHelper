"""
OAuth 2.0 驗證診斷工具
用於檢查 OAuth 設定和常見問題
"""
import json
import os
from pathlib import Path
from config import Config

def check_credentials_file():
    """檢查憑證檔案"""
    print("=" * 60)
    print("1. 檢查 OAuth 憑證檔案")
    print("=" * 60)
    
    config = Config()
    creds_file = Path(config.GOOGLE_SHEETS_CREDENTIALS_FILE)
    
    if not creds_file.exists():
        print(f"❌ 錯誤：找不到憑證檔案: {creds_file}")
        print(f"   請確認檔案路徑是否正確")
        return False
    
    print(f"✅ 憑證檔案存在: {creds_file}")
    
    try:
        with open(creds_file, 'r', encoding='utf-8') as f:
            secrets = json.load(f)
        
        if 'installed' in secrets:
            print("✅ 憑證類型：桌面應用程式")
            client_id = secrets['installed'].get('client_id', '')
            redirect_uris = secrets['installed'].get('redirect_uris', [])
        elif 'web' in secrets:
            print("✅ 憑證類型：網頁應用程式")
            client_id = secrets['web'].get('client_id', '')
            redirect_uris = secrets['web'].get('redirect_uris', [])
        else:
            print("❌ 錯誤：無法識別憑證類型（應包含 'installed' 或 'web'）")
            return False
        
        print(f"✅ 客戶端 ID: {client_id[:20]}...")
        print(f"✅ 憑證檔案中的重定向 URI: {redirect_uris}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ 錯誤：憑證檔案格式錯誤: {e}")
        return False
    except Exception as e:
        print(f"❌ 錯誤：讀取憑證檔案失敗: {e}")
        return False

def check_token_file():
    """檢查令牌檔案"""
    print("\n" + "=" * 60)
    print("2. 檢查 OAuth 令牌檔案")
    print("=" * 60)
    
    config = Config()
    token_file = Path(config.GOOGLE_SHEETS_TOKEN_FILE)
    
    if not token_file.exists():
        print("ℹ️  令牌檔案不存在（這是正常的，首次使用需要授權）")
        return True
    
    print(f"✅ 令牌檔案存在: {token_file}")
    
    try:
        with open(token_file, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        
        if 'refresh_token' in token_data:
            print("✅ 包含 refresh_token（可以刷新令牌）")
        else:
            print("⚠️  警告：沒有 refresh_token，可能需要重新授權")
        
        if 'expiry' in token_data:
            from datetime import datetime
            expiry = datetime.fromisoformat(token_data['expiry'].replace('Z', '+00:00'))
            now = datetime.now(expiry.tzinfo)
            if expiry > now:
                print(f"✅ 令牌尚未過期（到期時間: {expiry}）")
            else:
                print(f"⚠️  警告：令牌已過期（到期時間: {expiry}）")
        
        return True
        
    except Exception as e:
        print(f"⚠️  警告：讀取令牌檔案失敗: {e}")
        return True  # 這不是致命錯誤

def check_port():
    """檢查端口是否可用"""
    print("\n" + "=" * 60)
    print("3. 檢查端口 8080")
    print("=" * 60)
    
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        
        if result == 0:
            print("⚠️  警告：端口 8080 已被占用")
            print("   這可能導致 OAuth 授權失敗")
            print("   解決方法：關閉占用端口的程式")
            return False
        else:
            print("✅ 端口 8080 可用")
            return True
    except Exception as e:
        print(f"⚠️  警告：無法檢查端口: {e}")
        return True

def check_google_cloud_console_setup():
    """檢查 Google Cloud Console 設定建議"""
    print("\n" + "=" * 60)
    print("4. Google Cloud Console 設定檢查")
    print("=" * 60)
    
    config = Config()
    creds_file = Path(config.GOOGLE_SHEETS_CREDENTIALS_FILE)
    
    if not creds_file.exists():
        print("❌ 無法檢查：憑證檔案不存在")
        return
    
    try:
        with open(creds_file, 'r', encoding='utf-8') as f:
            secrets = json.load(f)
        
        if 'web' in secrets:
            print("📋 您使用的是「網頁應用程式」類型")
            print("\n請確認 Google Cloud Console 中已設定以下 URI：")
            print("\n【已授權的 JavaScript 來源】")
            print("  - http://localhost")
            print("  - http://localhost:8080")
            print("  - http://127.0.0.1")
            print("  - http://127.0.0.1:8080")
            print("\n【已授權的重新導向 URI】")
            print("  - http://localhost:8080/")
            print("  - http://localhost:8080")
            print("  - http://127.0.0.1:8080/")
            print("  - http://127.0.0.1:8080")
        elif 'installed' in secrets:
            print("📋 您使用的是「桌面應用程式」類型")
            print("\n請確認 Google Cloud Console 中已設定以下 URI：")
            print("\n【已授權的重新導向 URI】")
            print("  - http://localhost:8080/")
            print("  - http://localhost:8080")
            print("  - http://127.0.0.1:8080/")
            print("  - http://127.0.0.1:8080")
        
        print("\n⚠️  重要提示：")
        print("  1. 確保 URI 格式完全一致（包括斜線）")
        print("  2. 儲存設定後等待 1-2 分鐘再測試")
        print("  3. 如果仍失敗，查看瀏覽器地址欄中的實際 redirect_uri")
        
    except Exception as e:
        print(f"⚠️  無法讀取憑證檔案: {e}")

def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("OAuth 2.0 驗證診斷工具")
    print("=" * 60 + "\n")
    
    results = []
    
    # 檢查憑證檔案
    results.append(("憑證檔案", check_credentials_file()))
    
    # 檢查令牌檔案
    results.append(("令牌檔案", check_token_file()))
    
    # 檢查端口
    results.append(("端口 8080", check_port()))
    
    # Google Cloud Console 設定建議
    check_google_cloud_console_setup()
    
    # 總結
    print("\n" + "=" * 60)
    print("診斷總結")
    print("=" * 60)
    
    all_ok = all(result[1] for result in results)
    
    if all_ok:
        print("✅ 基本檢查通過")
        print("\n如果仍然出現驗證失敗，請：")
        print("1. 確認 Google Cloud Console 中的 URI 設定正確")
        print("2. 刪除舊的令牌檔案並重新授權")
        print("3. 查看實際錯誤訊息中的 redirect_uri")
    else:
        print("⚠️  發現問題，請根據上述建議修復")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()

