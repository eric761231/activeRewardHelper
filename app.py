from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from config import Config
from models import db, ActiveReward
from sync_service import SyncService
from sheets_service import GoogleSheetsService, SCOPES
import logging
from flask_cors import CORS
import os
from pathlib import Path

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config.from_object(Config())
# 設定 secret_key 用於 session（OAuth 流程需要）
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# CORS 設定：允許來自 Netlify 和其他前端的跨域請求
# 在生產環境中，建議使用環境變數來限制允許的來源
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

@app.route('/api/oauth/authorize', methods=['GET'])
def oauth_authorize():
    """
    啟動 OAuth 2.0 授權流程（Web 應用程式）
    用於 Render 等 Web 環境
    """
    try:
        config = Config()
        client_secrets_file = Path(config.GOOGLE_SHEETS_CREDENTIALS_FILE)
        
        if not client_secrets_file.exists():
            return jsonify({
                'success': False,
                'error': f'找不到 OAuth 2.0 客戶端憑證檔案: {client_secrets_file}'
            }), 500
        
        # 取得 Render URL 或使用請求的 host
        render_url = os.getenv('RENDER_EXTERNAL_URL', '')
        if not render_url:
            # 從請求中取得 base URL
            render_url = f"{request.scheme}://{request.host}"
        
        redirect_uri = f"{render_url}/oauth2callback"
        
        # 建立 OAuth 流程
        flow, authorization_url, state = GoogleSheetsService.create_web_flow(
            client_secrets_file,
            redirect_uri
        )
        
        # 儲存 state 到 session（用於回調驗證）
        session['oauth_state'] = state
        session['oauth_redirect_uri'] = redirect_uri  # 儲存 redirect_uri 以便回調時使用
        
        logging.info(f"OAuth 授權 URL: {authorization_url}")
        return redirect(authorization_url)
        
    except Exception as e:
        logging.exception("OAuth 授權失敗")
        return jsonify({
            'success': False,
            'error': f'OAuth 授權失敗: {str(e)}'
        }), 500

@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    """
    OAuth 2.0 回調處理
    處理 Google 重定向回來的授權結果
    """
    try:
        config = Config()
        client_secrets_file = Path(config.GOOGLE_SHEETS_CREDENTIALS_FILE)
        token_file = Path(config.GOOGLE_SHEETS_TOKEN_FILE)
        
        # 取得 Render URL
        render_url = os.getenv('RENDER_EXTERNAL_URL', '')
        if not render_url:
            render_url = f"{request.scheme}://{request.host}"
        
        redirect_uri = f"{render_url}/oauth2callback"
        
        # 從 session 取得 state（用於驗證）
        saved_state = session.get('oauth_state')
        saved_redirect_uri = session.get('oauth_redirect_uri', redirect_uri)
        
        if not saved_state:
            return jsonify({
                'success': False,
                'error': 'OAuth state 遺失，請重新授權'
            }), 400
        
        # 完成 OAuth 流程（使用 session 中儲存的 redirect_uri 和 state）
        authorization_response = request.url
        creds = GoogleSheetsService.complete_web_flow(
            client_secrets_file,
            saved_redirect_uri,
            authorization_response,
            state=saved_state
        )
        
        # 儲存憑證
        token_file.parent.mkdir(parents=True, exist_ok=True)
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())
        
        logging.info(f"OAuth 授權成功，憑證已儲存到: {token_file}")
        
        # 清除 session
        session.pop('oauth_state', None)
        session.pop('oauth_redirect_uri', None)
        
        # 重定向到首頁，顯示成功訊息
        return redirect(f'/?authorized=success')
        
    except Exception as e:
        logging.exception("OAuth 回調失敗")
        return jsonify({
            'success': False,
            'error': f'OAuth 回調失敗: {str(e)}'
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

