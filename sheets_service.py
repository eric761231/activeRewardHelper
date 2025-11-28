import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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
        第一次使用時，會在瀏覽器中打開授權頁面
        """
        client_secrets_file = Path(self.config.GOOGLE_SHEETS_CREDENTIALS_FILE)
        
        if not client_secrets_file.exists():
            raise FileNotFoundError(
                f"找不到 OAuth 2.0 客戶端憑證檔案: {client_secrets_file}\n"
                "請前往 Google Cloud Console 建立 OAuth 2.0 客戶端 ID 並下載憑證檔案。\n"
                "詳細說明請參考：OAUTH_SETUP.md"
            )
        
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_file),
            SCOPES
        )
        
        logger.info("正在啟動 OAuth 2.0 授權流程...")
        logger.info("瀏覽器將自動打開，請登入您的 Google 帳號並授權")
        
        # 在本地伺服器上運行授權流程
        creds = flow.run_local_server(port=0)
        
        logger.info("授權成功！")
        return creds
    
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

