from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.default import Config
import redis

db = SQLAlchemy()
# APP_SETTINGS = os.environ.get("APP_SETTINGS")
redis_store = None


def create_app():
    app = Flask(__name__)
    # 环境配置
    # app.config.from_object(APP_SETTINGS)
    app.config.from_object(Config)
    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

    db.init_app(app)
    migrate = Migrate(app, db)

    # 注册blueprint
    from MyApp.views import shorten
    app.register_blueprint(shorten)
    return app
