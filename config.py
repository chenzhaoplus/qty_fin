import os
from app.my_pymysql import DMysqlConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        # db_config = DMysqlConfig(app.config["DB_HOST"], app.config["DB_NAME"], app.config["DB_USER"],
        #                          app.config["DB_PWD"], app.config["DB_PORT"])
        # app.config["DB_CONFIG"] = db_config
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = 'v81'
    DB_PORT = 3306
    DB_NAME = 'python_crawl'
    DB_USER = 'root'
    DB_PWD = '123456'
    DB_CONFIG = DMysqlConfig(DB_HOST, DB_NAME, DB_USER, DB_PWD, DB_PORT)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or f'mysql+pymysql://%s:%s@%s:%d/%s' % (
        DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_NAME)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
