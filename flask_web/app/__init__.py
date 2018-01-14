#-*- coding:utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from smtplib import SMTP_SSL as SMTP
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
#项目原代码，使用flask-mail
# from flask_mail import Mail
#使用SMTP
from config import Config

bootstrap = Bootstrap()

#项目原代码，使用flask-mail
# mail = Mail()

#使用SMTP
# mail = SMTP(host=app.config['MAIL_SERVER'], port=app.config['MAIL_PORT'])
mail = SMTP(host=Config.MAIL_SERVER, port=Config.MAIL_PORT)

moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'    #None,'basic','strong'代表防止用户会话被篡改的不同安全等级
login_manager.login_view = 'auth.login'     #设置登录页面的端点,登录路由在蓝本中定义.所以要加上蓝本的名字

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    #项目原代码，使用flask-mail
    # mail.init_app(app)

    mail.set_debuglevel(False)

    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app