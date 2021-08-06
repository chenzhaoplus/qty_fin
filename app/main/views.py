import json

from flask import current_app

from app.utils.my_encoder import MyEncoder
from app.utils.my_pymysql import UsingMysql, init_dbconfig
from app.utils.my_sqlalchemy import UsingAlchemy
from . import main
from ..models import Product
from ..run_crawl import run_crawl
from ..utils.json_utils import ls_to_json


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


@main.route("/findAllProduct", methods=['GET'])
def findAllProduct():
    with UsingAlchemy() as ua:
        ls = ua.session.query(Product).all()

    return ls_to_json(ls)


@main.route("/findFirstProduct", methods=['GET'])
def findFirstProduct():
    with UsingAlchemy() as ua:
        obj = ua.session.query(Product).first()

    return obj.to_dict()


@main.route("/runCrawl", methods=['POST'])
def runCrawl():
    run_crawl()
    print('runCrawl success')
    return 'success'


@main.route("/findStockBySql", methods=['POST'])
def findStockBySql():
    with UsingMysql() as um:
        sql = """
            SELECT
                *
            FROM
                `test_stock_2021_08_06`
            WHERE
                `最新价` <= %s AND `总市值-数` >= %s
                AND `公司内在价值-净利润` <> ''
                AND `公司内在价值-营收` <> ''
            ORDER BY
                cast( `公司内在价值-净利润` AS DECIMAL(20,3) ) DESC
        """
        params = [30, 500 * 100000000]
        ls = um.fetch_all(sql, params)
    return json.dumps(ls)
