import json

from flask import current_app

from . import main
from ..my_encoder import MyEncoder
from ..my_pymysql import UsingMysql


@main.route('/', methods=['GET', 'POST'])
def home():
    print(f'SQLALCHEMY_DATABASE_URI = {current_app.config.get("SQLALCHEMY_DATABASE_URI")}')
    return 'Hello Home!'


@main.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'Hello World!'


@main.route("/findAllStock", methods=['POST'])
def findAllStock():
    with UsingMysql() as um:
        sql = 'select * from test_stock_2021_07_31'
        ls = um.fetch_all(sql)
    return json.dumps(ls, cls=MyEncoder)

# @main.route("/findAllProduct", methods=['GET'])
# def findAllProduct():
#     with UsingAlchemy() as ua:
#         ls = ua.session.query(Product).first()
#     return json.dumps(ls, cls=MyEncoder)
