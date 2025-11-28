"""
測試 OAuth 流程並捕獲實際使用的 redirect_uri
"""
import json
import logging
from pathlib import Path
from config import Config
from google_auth_oauthlib.flow import InstalledAppFlow
from sheets_service import SCOPES

# 設定日誌
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_oauth_flow():
    """測試 OAuth 流程"""
    print("=" * 60)
    print("OAuth 流程測試")
    print("=" * 60)
    
    config = Config()
    client_secrets_file = Path(config.GOOGLE_SHEETS_CREDENTIALS_FILE)
    
    if not client_secrets_file.exists():
        print(f"❌ 錯誤：找不到憑證檔案: {client_secrets_file}")
        return
    
    print(f"✅ 使用憑證檔案: {client_secrets_file}")
    
    # 讀取憑證檔案
    with open(client_secrets_file, 'r', encoding='utf-8') as f:
        secrets = json.load(f)
    
    # 如果是 web 類型，轉換為 installed 格式
    if 'web' in secrets and 'installed' not in secrets:
        print("📋 偵測到網頁應用程式類型，轉換為桌面應用程式格式")
        installed_secrets = {
            'installed': {
                'client_id': secrets['web']['client_id'],
                'client_secret': secrets['web']['client_secret'],
                'auth_uri': secrets['web']['auth_uri'],
                'token_uri': secrets['web']['token_uri'],
                'auth_provider_x509_cert_url': secrets['web'].get('auth_provider_x509_cert_url', ''),
                'client_x509_cert_url': secrets['web'].get('client_x509_cert_url', '')
            }
        }
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp_file:
            json.dump(installed_secrets, tmp_file, ensure_ascii=False, indent=2)
            tmp_file_path = tmp_file.name
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                tmp_file_path,
                SCOPES
            )
        finally:
            import os
            try:
                os.unlink(tmp_file_path)
            except:
                pass
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_file),
            SCOPES
        )
    
    print("\n" + "=" * 60)
    print("開始 OAuth 授權流程")
    print("=" * 60)
    print("\n⚠️  重要：請注意瀏覽器地址欄中的 redirect_uri")
    print("   當出現錯誤時，複製完整的錯誤 URL")
    print("   找到 redirect_uri= 後面的值，那就是實際使用的 URI")
    print("\n正在啟動授權流程（端口 8080）...\n")
    
    try:
        # 使用固定端口 8080
        creds = flow.run_local_server(port=8080, open_browser=True)
        print("\n✅ 授權成功！")
        print(f"✅ 使用的 redirect_uri: http://localhost:8080/")
        return creds
    except Exception as e:
        print(f"\n❌ 授權失敗: {e}")
        print("\n" + "=" * 60)
        print("故障排除")
        print("=" * 60)
        print("\n如果出現 redirect_uri_mismatch 錯誤：")
        print("1. 查看瀏覽器地址欄中的完整錯誤 URL")
        print("2. 找到 redirect_uri= 後面的值（例如：http://localhost:8080/）")
        print("3. 確保這個完全相同的 URI 已在 Google Cloud Console 中註冊")
        print("4. 注意：必須包含尾隨斜線 / 的版本和不包含的版本都要添加")
        print("\n常見問題：")
        print("- 實際使用: http://localhost:8080/ （帶斜線）")
        print("- 但 Google Cloud Console 中只有: http://localhost:8080 （不帶斜線）")
        print("- 解決：兩個版本都要添加！")
        raise

if __name__ == '__main__':
    try:
        test_oauth_flow()
    except KeyboardInterrupt:
        print("\n\n用戶取消操作")
    except Exception as e:
        print(f"\n\n錯誤: {e}")

