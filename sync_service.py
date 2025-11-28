from models import db, ActiveReward
from sheets_service import GoogleSheetsService
import logging

logger = logging.getLogger(__name__)

class SyncService:
    """資料同步服務"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
    
    def sync_data(self):
        """
        同步 Google Sheets 資料到資料庫
        1. 讀取未確認的資料
        2. 寫入資料庫
        3. 更新 Google Sheets 確認欄位
        """
        try:
            # 取得未確認的資料列
            unconfirmed_rows, headers, confirmed_col_idx = self.sheets_service.get_unconfirmed_rows()
            
            if not unconfirmed_rows:
                return {
                    'success': True,
                    'message': '沒有需要處理的資料',
                    'count': 0
                }
            
            success_count = 0
            error_count = 0
            
            # 處理每一筆資料
            for row_info in unconfirmed_rows:
                try:
                    row_data = row_info['data']
                    row_number = row_info['row_number']
                    
                    # 根據 headers 建立資料字典
                    data_dict = {}
                    for idx, header in enumerate(headers):
                        if idx < len(row_data):
                            data_dict[header] = row_data[idx]
                    
                    # 映射試算表欄位到資料庫欄位
                    # 試算表欄位：日期、執行代號、角色身分證、角色ID、道具編號、補償道具名稱、數量、已發放
                    reward = ActiveReward(
                        round=self._parse_int(data_dict.get('執行代號')),
                        char_id=data_dict.get('角色身分證'),
                        char_name=data_dict.get('角色ID'),
                        item_id=data_dict.get('道具編號'),
                        item_name=data_dict.get('補償道具名稱'),
                        item_count=self._parse_int(data_dict.get('數量')),
                        state=1  # 1 表示已發放（系統已發放給玩家）
                    )
                    
                    db.session.add(reward)
                    db.session.commit()
                    
                    # 更新 Google Sheets「已發放」欄位為 V
                    self.sheets_service.update_confirmation(row_number, confirmed_col_idx)
                    
                    success_count += 1
                    
                except Exception as e:
                    db.session.rollback()
                    logger.error(f"處理第 {row_number} 行資料時發生錯誤: {str(e)}")
                    error_count += 1
                    continue
            
            message = f'發放完成！成功處理 {success_count} 筆資料'
            if error_count > 0:
                message += f'，{error_count} 筆失敗'
            
            return {
                'success': True,
                'message': message,
                'count': success_count,
                'error_count': error_count
            }
            
        except Exception as e:
            logger.error(f"同步資料失敗: {str(e)}")
            return {
                'success': False,
                'message': f'同步失敗: {str(e)}',
                'count': 0
            }
    
    def _parse_int(self, value_str):
        """解析整數字串為整數"""
        if not value_str:
            return None
        try:
            # 移除可能的逗號和空白
            cleaned = str(value_str).replace(',', '').strip()
            return int(cleaned)
        except (ValueError, TypeError):
            return None

