import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # 設定檔路徑
        config_dir = Path(__file__).parent / 'config'
        mysql_config_path = config_dir / 'mysql_config.json'
        cloud_config_path = config_dir / 'cloud_csv_config.json'
        
        # 讀取 MySQL 設定
        self._load_mysql_config(mysql_config_path)
        
        # 讀取 Google Sheets 設定
        self._load_cloud_config(cloud_config_path)
        
        # Flask 設定（仍使用環境變數或預設值）
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    def _load_mysql_config(self, config_path):
        """讀取 MySQL 設定檔"""
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    mysql_config = json.load(f)
                    self.DB_HOST = mysql_config.get('host', 'localhost')
                    self.DB_PORT = int(mysql_config.get('port', 3306))
                    self.DB_USER = mysql_config.get('user', 'root')
                    self.DB_PASSWORD = mysql_config.get('password', '')
                    self.DB_NAME = mysql_config.get('database', 'active_reward_db')
                    self.DB_CHARSET = mysql_config.get('charset', 'utf8mb4')
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"警告：讀取 MySQL 設定檔失敗，使用預設值: {e}")
                self._set_default_mysql_config()
        else:
            print(f"警告：找不到 MySQL 設定檔 {config_path}，使用預設值")
            self._set_default_mysql_config()
    
    def _set_default_mysql_config(self):
        """設定預設 MySQL 設定"""
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT = int(os.getenv('DB_PORT', 3306))
        self.DB_USER = os.getenv('DB_USER', 'root')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        self.DB_NAME = os.getenv('DB_NAME', 'active_reward_db')
        self.DB_CHARSET = 'utf8mb4'
    
    def _load_cloud_config(self, config_path):
        """讀取 Google Sheets 設定檔"""
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    cloud_config = json.load(f)
                    self.GOOGLE_SHEETS_CREDENTIALS_FILE = cloud_config.get('credentials_file', 'credentials.json')
                    self.SPREADSHEET_ID = cloud_config.get('spreadsheet_id', '')
                    self.WORKSHEET_NAME = cloud_config.get('worksheet_name', '')
                    self.WORKSHEET_GID = cloud_config.get('worksheet_gid', '')
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"警告：讀取 Google Sheets 設定檔失敗，使用預設值: {e}")
                self._set_default_cloud_config()
        else:
            print(f"警告：找不到 Google Sheets 設定檔 {config_path}，使用預設值")
            self._set_default_cloud_config()
    
    def _set_default_cloud_config(self):
        """設定預設 Google Sheets 設定"""
        self.GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
        self.SPREADSHEET_ID = os.getenv('SPREADSHEET_ID', '1T70siVXhG8VcERTGtVKiSdWPfc6eHc4dt-SGOt9ppE4')
        self.WORKSHEET_NAME = os.getenv('WORKSHEET_NAME', '神說外交官')
        self.WORKSHEET_GID = os.getenv('WORKSHEET_GID', '1753592588')
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"

