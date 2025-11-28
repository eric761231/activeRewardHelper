#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具腳本：還原 Google Sheet 中指定行的「已發放」欄位為空白
用於還原被誤處理的資料
"""

import sys
from sheets_service import GoogleSheetsService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def restore_rows(row_numbers):
    """
    還原指定行的「已發放」欄位為空白
    
    Args:
        row_numbers: 要還原的行號列表（例如：[141, 230, 231]）
    """
    try:
        sheets_service = GoogleSheetsService()
        
        # 取得工作表資訊
        all_values = sheets_service.worksheet.get_all_values()
        if not all_values or len(all_values) < 2:
            print("錯誤：工作表沒有資料")
            return False
        
        headers = all_values[0]
        
        # 找到「已發放」欄位的索引
        confirmed_col_idx = None
        for idx, header in enumerate(headers):
            if '已發放' in header or 'issued' in header.lower() or 'confirmed' in header.lower():
                confirmed_col_idx = idx
                break
        
        if confirmed_col_idx is None:
            print("錯誤：找不到「已發放」欄位")
            return False
        
        # 還原每一行
        success_count = 0
        for row_number in row_numbers:
            try:
                # 檢查行號是否有效
                if row_number < 2 or row_number > len(all_values):
                    print(f"警告：行號 {row_number} 超出範圍（有效範圍：2-{len(all_values)}），跳過")
                    continue
                
                # 取得當前值
                row_data = all_values[row_number - 1]  # 轉換為 0-based 索引
                current_value = ''
                if len(row_data) > confirmed_col_idx:
                    current_value = row_data[confirmed_col_idx].strip()
                
                # 如果已經是空白，跳過
                if not current_value:
                    print(f"行 {row_number}：已經是空白，跳過")
                    continue
                
                # 還原為空白
                col_letter = sheets_service._number_to_column_letter(confirmed_col_idx + 1)
                cell_address = f"{col_letter}{row_number}"
                sheets_service.worksheet.update(cell_address, '')
                
                print(f"✓ 已還原行 {row_number} 的「已發放」欄位為空白（原值：'{current_value}'）")
                success_count += 1
                
            except Exception as e:
                print(f"✗ 還原行 {row_number} 失敗：{str(e)}")
                continue
        
        print(f"\n完成！成功還原 {success_count} 行")
        return True
        
    except Exception as e:
        print(f"錯誤：{str(e)}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("Google Sheet 資料還原工具")
    print("=" * 60)
    print("\n此工具會將指定行的「已發放」欄位還原為空白")
    print("請輸入要還原的行號（用逗號分隔，例如：141,230,231）")
    print("\n輸入 'q' 或 'quit' 退出")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n請輸入行號（用逗號分隔）: ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("退出程式")
                break
            
            if not user_input:
                print("請輸入行號")
                continue
            
            # 解析行號
            try:
                row_numbers = [int(x.strip()) for x in user_input.split(',') if x.strip()]
            except ValueError:
                print("錯誤：行號必須是數字")
                continue
            
            if not row_numbers:
                print("錯誤：沒有有效的行號")
                continue
            
            # 確認
            print(f"\n將還原以下 {len(row_numbers)} 行的「已發放」欄位為空白：")
            print(f"  行號：{', '.join(map(str, row_numbers))}")
            confirm = input("\n確認執行？(y/n): ").strip().lower()
            
            if confirm != 'y':
                print("已取消")
                continue
            
            # 執行還原
            print("\n開始還原...")
            restore_rows(row_numbers)
            
            # 詢問是否繼續
            continue_input = input("\n是否繼續還原其他行？(y/n): ").strip().lower()
            if continue_input != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\n程式已中斷")
            break
        except Exception as e:
            print(f"發生錯誤：{str(e)}")
            continue

if __name__ == '__main__':
    # 如果提供了命令行參數，直接執行
    if len(sys.argv) > 1:
        try:
            row_numbers = [int(x) for x in sys.argv[1:]]
            restore_rows(row_numbers)
        except ValueError:
            print("錯誤：行號必須是數字")
            print("用法：python restore_sheet_rows.py <行號1> <行號2> ...")
            print("例如：python restore_sheet_rows.py 141 230 231")
    else:
        # 互動模式
        main()

