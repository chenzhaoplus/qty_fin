from flask import Flask
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import app.utils.date_utils as du
# from logger_config import fh, sh

# moment = Moment()
db = SQLAlchemy()


# basedir = os.path.abspath(os.path.dirname(__name__))


# def config_logger(app):
#     logging.basicConfig(
#         level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
#         format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
#         datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
#         filename=f'{basedir}\\logging{du.get_cur_date("%Y-%m-%d")}.log',  # log文件名
#         filemode='w')  # 写入模式“w”或“a”
#
#     # Define a Handler and set a format which output to console
#     # console = logging.StreamHandler()  # 定义console handler
#     console = logging.FileHandler(f'logging{du.get_cur_date("%Y-%m-%d")}.log', encoding='UTF-8')
#     console.setLevel(logging.INFO)  # 定义该handler级别
#     formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
#     console.setFormatter(formatter)
#     app.logger.addHandler(console)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # moment.init_app(app)
    db.init_app(app)

    # 添加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 设置日志
    # config_logger(app)
    # app.logger.addHandler(fh)
    # app.logger.addHandler(sh)

    return app
