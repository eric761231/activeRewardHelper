import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from config import Config
import logging
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# OAuth 2.0 所需的權限範圍
SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# 全域變數：用於儲存 Web OAuth 流程的 state（用於回調驗證）
_oauth_flow_state = None

class GoogleSheetsService:
    """Google Sheets 服務類別（使用個人 Google 帳號 OAuth 2.0）"""
    
    def __init__(self):
        self.config = Config()
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self._connect()
    
    def _get_credentials(self):
        """
        取得 OAuth 2.0 憑證
        如果已有儲存的令牌，使用它；否則進行授權流程
        """
        creds = None
        token_file = Path(self.config.GOOGLE_SHEETS_TOKEN_FILE)
        
        # 檢查是否已有儲存的令牌
        if token_file.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
                logger.info("從檔案載入已儲存的憑證")
            except Exception as e:
                logger.warning(f"載入已儲存的憑證失敗: {e}")
                creds = None
        
        # 如果沒有憑證或憑證已過期
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # 嘗試刷新令牌
                try:
                    logger.info("令牌已過期，正在刷新...")
                    creds.refresh(Request())
                    logger.info("令牌刷新成功")
                except Exception as e:
                    logger.warning(f"刷新令牌失敗: {e}，需要重新授權")
                    creds = None
            
            # 如果仍然沒有有效的憑證，進行授權流程
            if not creds or not creds.valid:
                logger.info("需要進行 OAuth 2.0 授權流程")
                creds = self._authorize()
        
        # 儲存憑證供下次使用
        if creds and creds.valid:
            try:
                with open(token_file, 'w', encoding='utf-8') as token:
                    token.write(creds.to_json())
                logger.info(f"憑證已儲存到: {token_file}")
            except Exception as e:
                logger.warning(f"儲存憑證失敗: {e}")
        
        return creds
    
    def _authorize(self):
        """
        執行 OAuth 2.0 授權流程
        自動偵測憑證檔案類型並使用對應的流程
        """
        client_secrets_file = Path(self.config.GOOGLE_SHEETS_CREDENTIALS_FILE)
        
        if not client_secrets_file.exists():
            raise FileNotFoundError(
                f"找不到 OAuth 2.0 客戶端憑證檔案: {client_secrets_file}\n"
                "請前往 Google Cloud Console 建立 OAuth 2.0 客戶端 ID 並下載憑證檔案。\n"
                "詳細說明請參考：OAUTH_SETUP.md"
            )
        
        # 檢查憑證檔案類型
        try:
            with open(client_secrets_file, 'r', encoding='utf-8') as f:
                secrets = json.load(f)
            
            # 偵測憑證檔案類型
            if 'installed' in secrets:
                # 桌面應用程式類型
                logger.info("偵測到桌面應用程式類型的憑證檔案")
                return self._authorize_desktop(client_secrets_file)
            elif 'web' in secrets:
                # 網頁應用程式類型
                logger.info("偵測到網頁應用程式類型的憑證檔案，使用 Web 流程")
                return self._authorize_web_local(client_secrets_file)
            else:
                raise ValueError("無法識別憑證檔案類型（應包含 'installed' 或 'web' 鍵）")
        except json.JSONDecodeError as e:
            raise ValueError(f"憑證檔案格式錯誤: {e}")
    
    def _authorize_web_local(self, client_secrets_file):
        """
        網頁應用程式 OAuth 流程（本地開發，使用 localhost）
        注意：即使憑證檔案是 web 類型，在本地開發時也使用 InstalledAppFlow
        因為它會自動處理 localhost 回調，更簡單
        """
        logger.info("雖然憑證檔案是網頁應用程式類型，但在本地開發時使用桌面應用程式流程")
        logger.info("這會自動處理 localhost 回調，無需手動設定重定向 URI")
        
        # 對於本地開發，即使憑證檔案是 web 類型，也使用 InstalledAppFlow
        # 因為 InstalledAppFlow 會自動處理 localhost 回調
        # 但需要將 web 類型的憑證轉換為 installed 格式
        
        try:
            # 讀取憑證檔案
            with open(client_secrets_file, 'r', encoding='utf-8') as f:
                secrets = json.load(f)
            
            # 如果是 web 類型，轉換為 installed 格式（臨時）
            if 'web' in secrets and 'installed' not in secrets:
                logger.info("將網頁應用程式憑證轉換為桌面應用程式格式（僅用於本地開發）")
                # 建立臨時的 installed 格式憑證
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
                
                # 使用臨時憑證建立 InstalledAppFlow
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
                    # 清理臨時檔案
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
            else:
                # 如果已經是 installed 格式，直接使用
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(client_secrets_file),
                    SCOPES
                )
            
            logger.info("正在啟動 OAuth 2.0 授權流程（本地開發）...")
            logger.info("瀏覽器將自動打開，請登入您的 Google 帳號並授權")
            
            # 嘗試多個固定端口
            fixed_ports = [8080, 8081, 8082, 8083, 8084]
            creds = None
            
            for port in fixed_ports:
                try:
                    logger.info(f"嘗試使用端口 {port}...")
                    creds = flow.run_local_server(port=port)
                    logger.info(f"成功使用端口 {port}")
                    break
                except OSError as e:
                    logger.debug(f"端口 {port} 被占用: {e}")
                    continue
            
            if not creds:
                # 如果所有固定端口都被占用，使用自動選擇端口
                logger.warning("所有固定端口都被占用，使用自動選擇端口")
                logger.warning("請確保 Google Cloud Console 中有該 URI")
                creds = flow.run_local_server(port=0)
            
            logger.info("授權成功！")
            return creds
            
        except Exception as e:
            logger.error(f"授權失敗: {e}")
            raise
    
    def _authorize_desktop(self, client_secrets_file):
        """桌面應用程式 OAuth 流程（本地開發）"""
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_file),
            SCOPES
        )
        
        logger.info("正在啟動 OAuth 2.0 授權流程（桌面應用程式）...")
        logger.info("瀏覽器將自動打開，請登入您的 Google 帳號並授權")
        
        # 在本地伺服器上運行授權流程
        # 嘗試多個固定端口，避免使用隨機端口（導致 redirect_uri_mismatch）
        fixed_ports = [8080, 8081, 8082, 8083, 8084]
        creds = None
        
        for port in fixed_ports:
            try:
                logger.info(f"嘗試使用端口 {port}...")
                creds = flow.run_local_server(port=port)
                logger.info(f"成功使用端口 {port}")
                break
            except OSError as e:
                logger.debug(f"端口 {port} 被占用: {e}")
                continue
        
        if not creds:
            # 如果所有固定端口都被占用，使用自動選擇端口
            logger.warning("所有固定端口都被占用，使用自動選擇端口（可能導致 redirect_uri_mismatch）")
            logger.warning("建議：1) 關閉占用端口的程式 2) 或在 Google Cloud Console 中添加實際使用的 URI")
            logger.warning("如果出現 redirect_uri_mismatch 錯誤，請查看授權 URL 中的端口號，並添加到 Google Cloud Console")
            creds = flow.run_local_server(port=0)
        
        logger.info("授權成功！")
        return creds
    
    @staticmethod
    def create_web_flow(client_secrets_file, redirect_uri):
        """
        建立 Web 應用程式 OAuth 流程
        用於 Flask 路由中
        
        Returns:
            tuple: (flow, authorization_url, state)
        """
        flow = Flow.from_client_secrets_file(
            str(client_secrets_file),
            SCOPES,
            redirect_uri=redirect_uri
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'  # 強制顯示同意畫面，確保獲得 refresh_token
        )
        
        return flow, authorization_url, state
    
    @staticmethod
    def complete_web_flow(client_secrets_file, redirect_uri, authorization_response, state=None):
        """
        完成 Web 應用程式 OAuth 流程
        用於 Flask 回調路由中
        
        Args:
            client_secrets_file: OAuth 客戶端憑證檔案路徑
            redirect_uri: 重定向 URI（必須與建立流程時一致）
            authorization_response: 授權回應 URL（從 request.url 取得）
            state: OAuth state（從 session 取得，用於驗證）
        """
        flow = Flow.from_client_secrets_file(
            str(client_secrets_file),
            SCOPES,
            redirect_uri=redirect_uri,
            state=state
        )
        
        flow.fetch_token(authorization_response=authorization_response)
        return flow.credentials
    
    def _connect(self):
        """連接到 Google Sheets"""
        try:
            # 使用 OAuth 2.0 憑證
            creds = self._get_credentials()
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(self.config.SPREADSHEET_ID)
            
            # 優先根據工作表名稱查找
            if hasattr(self.config, 'WORKSHEET_NAME') and self.config.WORKSHEET_NAME:
                for sheet in self.spreadsheet.worksheets():
                    if sheet.title == self.config.WORKSHEET_NAME:
                        self.worksheet = sheet
                        logger.info(f"根據名稱找到工作表: {self.config.WORKSHEET_NAME}")
                        break
            
            # 如果根據名稱找不到，嘗試根據 GID 查找
            if not self.worksheet and hasattr(self.config, 'WORKSHEET_GID') and self.config.WORKSHEET_GID:
                for sheet in self.spreadsheet.worksheets():
                    if str(sheet.id) == str(self.config.WORKSHEET_GID):
                        self.worksheet = sheet
                        logger.info(f"根據 GID 找到工作表: {self.config.WORKSHEET_GID}")
                        break
            
            # 如果都找不到，使用第一個工作表
            if not self.worksheet:
                self.worksheet = self.spreadsheet.sheet1
                logger.warning(f"找不到指定名稱或 GID 的工作表，使用第一個工作表: {self.worksheet.title}")
            
            logger.info(f"成功連接到 Google Sheets: {self.worksheet.title}")
            
        except Exception as e:
            logger.error(f"連接 Google Sheets 失敗: {str(e)}")
            raise
    
    def get_unconfirmed_rows(self):
        """
        取得未確認的資料列（「已發放」欄位為空白的資料）
        只處理空白欄位，跳過已有 V 或其他文字的資料
        假設第一列是標題，第二列開始是資料
        需要根據實際試算表結構調整欄位索引
        """
        try:
            all_values = self.worksheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return [], [], None
            
            headers = all_values[0]
            
            # 找到「已發放」欄位的索引（確認欄位）
            confirmed_col_idx = None
            for idx, header in enumerate(headers):
                if '已發放' in header or 'issued' in header.lower() or 'confirmed' in header.lower():
                    confirmed_col_idx = idx
                    break
            
            if confirmed_col_idx is None:
                logger.warning("找不到「已發放」欄位，無法判斷哪些資料需要處理")
                # 如果找不到確認欄位，返回空列表（避免誤處理）
                return [], headers, None
            
            unconfirmed_rows = []
            for row_idx, row in enumerate(all_values[1:], start=2):  # start=2 因為第一列是標題
                if len(row) > confirmed_col_idx:
                    confirmed_value = row[confirmed_col_idx].strip()
                    # 只處理「已發放」欄位為空白的資料（跳過已有 V 或其他文字的資料）
                    if not confirmed_value or confirmed_value == '':
                        unconfirmed_rows.append({
                            'row_number': row_idx,
                            'data': row,
                            'confirmed_col_idx': confirmed_col_idx
                        })
            
            return unconfirmed_rows, headers, confirmed_col_idx
            
        except Exception as e:
            logger.error(f"讀取 Google Sheets 資料失敗: {str(e)}")
            raise
    
    def update_confirmation(self, row_number, confirmed_col_idx):
        """
        更新指定列的「已發放」欄位為 V
        """
        try:
            if confirmed_col_idx is not None:
                # 使用 A1 表示法更新儲存格（row_number 是實際行號，confirmed_col_idx+1 是欄位編號）
                col_letter = self._number_to_column_letter(confirmed_col_idx + 1)
                cell_address = f"{col_letter}{row_number}"
                self.worksheet.update(cell_address, 'V')
                logger.info(f"已更新第 {row_number} 行的「已發放」欄位為 V")
            else:
                logger.warning("找不到「已發放」欄位，無法更新")
        except Exception as e:
            logger.error(f"更新「已發放」欄位失敗: {str(e)}")
            raise
    
    def _number_to_column_letter(self, n):
        """將數字轉換為 Excel 欄位字母（1->A, 2->B, ..., 27->AA）"""
        result = ""
        while n > 0:
            n -= 1
            result = chr(65 + (n % 26)) + result
            n //= 26
        return result

