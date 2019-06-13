from MyApp import db
from sqlalchemy import func
from sqlalchemy_utils.types.choice import ChoiceType


class ShortCodes(db.Model):
    __tablename__ = "short_codes"
    TYPES = [('system', 'system'),
             ('custom', 'custom')]
    id = db.Column(db.Integer, primary_key=True, comment='id')
    redis_incr_id = db.Column(db.Integer, comment='redis自增id')
    url = db.Column(db.String(1000), nullable=False, comment='长网址')
    code = db.Column(db.String(6), nullable=False, comment='短链接')
    hit_count = db.Column(db.Integer, default=0, comment='点击次数')
    type = db.Column(ChoiceType(TYPES), default=TYPES[0][0], comment='类型')
    created_at = db.Column(db.DateTime, server_default=func.now(), comment='创建时间')
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def get_cope(self):
        return self.code

    def get_url(self):
        return self.url
