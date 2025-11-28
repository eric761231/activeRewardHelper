import gspread
from google.oauth2.service_account import Credentials
from config import Config
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    """Google Sheets 服務類別"""
    
    def __init__(self):
        self.config = Config()
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self._connect()
    
    def _connect(self):
        """連接到 Google Sheets"""
        try:
            # 使用服務帳號憑證
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(
                self.config.GOOGLE_SHEETS_CREDENTIALS_FILE,
                scopes=scope
            )
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

