from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ActiveReward(db.Model):
    """active_reward 資料表模型"""
    __tablename__ = 'active_reward'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round = db.Column(db.Integer, nullable=True)  # 執行代號
    char_id = db.Column(db.String(255), nullable=True)  # 角色身分證
    char_name = db.Column(db.String(255), nullable=True)  # 角色ID
    item_id = db.Column(db.String(255), nullable=True)  # 道具編號
    item_name = db.Column(db.String(255), nullable=True)  # 補償道具名稱
    item_count = db.Column(db.Integer, nullable=True)  # 數量
    item_obj_id = db.Column(db.Integer, default=0, nullable=True)
    item_enchant = db.Column(db.Integer, default=0, nullable=True)
    materials = db.Column(db.Integer, default=0, nullable=True)
    materials_count = db.Column(db.Integer, default=0, nullable=True)
    exp = db.Column(db.Integer, default=0, nullable=True)
    state = db.Column(db.Integer, default=1, nullable=True)  # 狀態 (1=已發放, 2=玩家已領取)
    end_time = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'round': self.round,
            'char_id': self.char_id,
            'char_name': self.char_name,
            'item_id': self.item_id,
            'item_name': self.item_name,
            'item_count': self.item_count,
            'item_obj_id': self.item_obj_id,
            'item_enchant': self.item_enchant,
            'materials': self.materials,
            'materials_count': self.materials_count,
            'exp': self.exp,
            'state': self.state,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }

