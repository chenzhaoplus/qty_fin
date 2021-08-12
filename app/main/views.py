import json

from flask import current_app
from flask import current_app as cur_app
from flask import request

import app.utils.constants as const
from app.utils.my_encoder import MyEncoder
from app.utils.my_pymysql import UsingMysql
from app.utils.my_sqlalchemy import UsingAlchemy
from app.utils.page_utils import get_cnt_sql, get_page_sql
from . import main
from ..models import Product
from ..run_crawl import run_crawl
from ..sql import mapper
from ..utils.json_utils import ls_to_json


@main.route("/findStockBySql", methods=['POST'])
def findStockBySql():
    form_json = request.json
    gpmc = form_json.get(const.gpmc[1])
    gpdm = form_json.get(const.gpdm[1])
    gplx = form_json.get(const.gplx[1])
    zxj_low = form_json.get('zxjLow')
    zxj_high = form_json.get('zxjHigh')
    gp_report = form_json.get('gp_report')
    zsz_low = float(form_json.get('zszLow') * 1_0000_0000) if form_json.get('zszLow') is not None else None
    zsz_high = float(form_json.get('zszHigh') * 1_0000_0000) if form_json.get('zszHigh') is not None else None
    table_name = f'`{const.TABLE_PREFIX}_{gp_report}`'
    sql = mapper.findStockBySql(table_name)
    count_key = 'count(1)'
    with UsingMysql() as um:
        params = [
            f'%{gpmc}%', gpmc,
            f'%{gpdm}%', gpdm,
            gplx, gplx,
            zxj_low, zxj_low,
            zxj_high, zxj_high,
            zsz_low, zsz_low,
            zsz_high, zsz_high]
        cur_app.logger.info(f'params: {params}')
        ls = um.fetch_all(get_page_sql(request, sql), params)
        cnt = um.get_count(get_cnt_sql(sql, count_key), params, count_key=count_key)
    return json.dumps({
        "content": ls,
        "totalElements": cnt
    }, cls=MyEncoder)


@main.route('/findGplxAll', methods=['GET', 'POST'])
def findGplxAll():
    form_json = request.json
    gplx = form_json.get(const.gplx[1])
    with UsingMysql() as um:
        params = [f'%{gplx}%', gplx]
        sql = mapper.findGplxAll()
        ls = um.fetch_all(sql, params)
    return json.dumps(ls, cls=MyEncoder)


@main.route('/findStockTable', methods=['GET', 'POST'])
def findStockTable():
    form_json = request.json
    keyword = form_json.get('keyword')
    with UsingMysql() as um:
        params = [f'%{const.TABLE_PREFIX}_%',
                  f'%{const.TABLE_PREFIX}_{keyword}%', f'{keyword}']
        sql = mapper.findStockTable()
        ls = um.fetch_all(sql, params)
    ret = [str(x['table_name']).replace(f'{const.TABLE_PREFIX}_', '') for x in ls]
    return json.dumps(ret, cls=MyEncoder)


@main.route('/', methods=['GET', 'POST'])
def home():
    cur_app.logger.info(f'SQLALCHEMY_DATABASE_URI = {current_app.config.get("SQLALCHEMY_DATABASE_URI")}')
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
    cur_app.logger.info('runCrawl success')
    return 'success'
