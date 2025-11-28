from flask import Flask, render_template, jsonify, request
from config import Config
from models import db, ActiveReward
from sync_service import SyncService
import logging
from flask_cors import CORS

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config.from_object(Config())
# CORS 設定：允許來自 Netlify 和其他前端的跨域請求
# 在生產環境中，建議使用環境變數來限制允許的來源
import os
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
db.init_app(app)

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/api/sync', methods=['POST'])
def sync():
    """同步資料 API"""
    try:
        sync_service = SyncService()
        result = sync_service.sync_data()
        return jsonify(result)
    except Exception as e:
        # 記錄完整 traceback 以供除錯
        import traceback
        logging.exception("同步 API 錯誤")
        tb = traceback.format_exc()
        # 回傳簡短訊息與詳細 traceback（開發用），避免在生產環境揭露敏感資訊
        return jsonify({
            'success': False,
            'message': f'發生錯誤: {str(e)}',
            'detail': tb,
            'count': 0
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """取得系統狀態"""
    try:
        # 測試資料庫連接
        count = ActiveReward.query.count()
        return jsonify({
            'success': True,
            'database_connected': True,
            'total_records': count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'database_connected': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 預設 DB 可用性為 False，啟動時檢查後再更新
    app.config['DB_AVAILABLE'] = False

    with app.app_context():
        try:
            # 如果使用 MySQL，嘗試在伺服器上建立資料庫（如果不存在）
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_uri and db_uri.startswith('mysql'):
                try:
                    import pymysql

                    host = app.config.get('DB_HOST', 'localhost')
                    port = int(app.config.get('DB_PORT', 3306))
                    user = app.config.get('DB_USER', 'root')
                    password = app.config.get('DB_PASSWORD', '')
                    db_name = app.config.get('DB_NAME', '')
                    charset = app.config.get('DB_CHARSET', 'utf8mb4')

                    conn = pymysql.connect(host=host, port=port, user=user, password=password, charset=charset)
                    with conn.cursor() as cur:
                        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET {charset}")
                    conn.commit()
                    conn.close()
                    logging.info(f"確保資料庫存在: {db_name}")
                except Exception as e:
                    logging.error(f"無法建立或連線到 MySQL 伺服器: {e}")

            # 嘗試建立資料表（如果連線失敗會拋出例外）
            try:
                db.create_all()
                app.config['DB_AVAILABLE'] = True
                logging.info('資料表建立檢查完成，DB 可用')
            except Exception as e:
                app.config['DB_AVAILABLE'] = False
                logging.error(f'建立資料表失敗，DB 可能不可用: {e}')

        except Exception as e:
            app.config['DB_AVAILABLE'] = False
            logging.error(f"啟動時檢查資料庫發生未預期錯誤: {e}")

    app.run(debug=True, host='0.0.0.0', port=2998)

