import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    MAIL_USE_TLS = True
    #使用SMTP
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    FLASKY_MAIL_SENDER = '1332369530@qq.com'
    MAIL_USERNAME = "Z_Ling"
    MAIL_PASSWORD = "xpicawvfucvtbaea"
    FLASKY_ADMIN = 'ZERO'
    #项目原代码，使用flask-mail
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # FLASKY_MAIL_SENDER = 'Flasky Admin <zero141104@gmail.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    #原代码修改(运行不报错，但是收不到邮件)
    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_PORT = 465
    # MAIL_USERNAME = 'Z_Ling'
    # MAIL_PASSWORD = 'xpicawvfucvtbaea'
    # FLASKY_MAIL_SENDER = '1332369530@qq.com'
    # FLASKY_ADMIN = 'ZERO'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
