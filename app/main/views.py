import json

from flask import current_app
from flask import request

from app.utils.my_encoder import MyEncoder
from app.utils.my_pymysql import UsingMysql
from app.utils.my_sqlalchemy import UsingAlchemy
from app.utils.page_utils import get_page_params, get_cnt_sql, get_page_sql
from . import main
from ..models import Product
from ..run_crawl import run_crawl
from ..sql import mapper
from ..utils.json_utils import ls_to_json


@main.route("/findStockBySql", methods=['POST'])
def findStockBySql():
    form_json = request.json
    stock_name = form_json.get("stockName")
    stock_code = form_json.get("stockCode")
    stock_type = form_json.get("stockType")
    sql = mapper.findStockBySql()
    count_key = 'count(1)'
    with UsingMysql() as um:
        params = [30, 30,
                  500 * 100000000, 500 * 100000000,
                  f'%{stock_name}%', stock_name,
                  f'%{stock_code}%', stock_code,
                  stock_type, stock_type]
        print(f'params: {params}')
        ls = um.fetch_all(get_page_sql(request, sql), params)
        cnt = um.get_count(get_cnt_sql(sql, count_key), params, count_key=count_key)
    return {
        "content": ls,
        "totalElements": cnt
    }


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
        sql = 'select * from stock_info_2021_07_31'
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
