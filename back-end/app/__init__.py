from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


# Flask-SQLAlchemy plugin
db = SQLAlchemy()
# Flask-Migrate plugin
migrate = Migrate()

'''
创建flask应用p
'''
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    '''
    注册flask-cors, 用于跨域配置，因为前端是8000端口，后端是5000端口，将他们关联起来
    '''
    CORS(app)
    '''
    注册数据库
    '''
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)

    '''
    注册蓝图 blueprint
    '''
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models
