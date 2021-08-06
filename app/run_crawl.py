import os

import pandas as pd
from sqlalchemy import types

import app.crawl.dfcf.analysis_crawl as analysis
import app.crawl.dfcf.code_crawl as code
import app.crawl.dfcf.detail_crawl as detail
import app.crawl.dfcf.finance_crawl as finance
import app.utils.constants as const
import app.utils.date_utils as du
from app.crawl.browser_pool import BrowserPool
from app.utils.async_utils import async_able
from app.utils.my_sqlalchemy import init_engine

# cur_year = du.get_cur_date("%Y")
cur_year = '2021'

# cur_m_d = '07-31'
cur_m_d = du.get_cur_date("%m-%d")

cur_y_m_d = f'{cur_year}-{cur_m_d}'

basedir = os.path.abspath(os.path.dirname(__file__))


def basic_file(type_name):
    return f'{basedir}/res/{cur_year}/{cur_m_d}/{type_name}股票基本信息{cur_y_m_d}.csv'


def analysis_file(type_name):
    return f'{basedir}/res/{cur_year}/{cur_m_d}/{type_name}股票分析信息{cur_y_m_d}.csv'


def code_crawl(type_name, url, pool):
    write_file = basic_file(type_name)
    code.begin_crawl(write_file, pool, url, type_name)


def detail_crawl(type_name, pool):
    read_file = basic_file(type_name)
    write_file = basic_file(type_name)
    detail.begin_crawl(read_file, write_file, pool, type_name)


def finance_crawl(type_name, pool):
    read_file = basic_file(type_name)
    write_file = basic_file(type_name)
    finance.begin_crawl(read_file, write_file, pool, type_name)


def analysis_crawl(type_name, pool):
    read_file = basic_file(type_name)
    write_file = analysis_file(type_name)
    analysis.begin_crawl(read_file, write_file, pool, by=const.gsnzjz_jlr, type_name=type_name)


def mysql_crawl(pls):
    cat_ls = []
    for p in pls:
        read_file = analysis_file(p[0])
        data = pd.read_csv(read_file, dtype='object')  # dtype='object' 读取时转成字符串
        cat_ls.append(data)
    df = pd.concat(cat_ls, ignore_index=True)
    # df.loc[df['营收同比率'] == '-'] = ''
    # df.loc[df['净利润同比'] == '-'] = ''
    # df["股票代码"] = np.where(len(df.股票代码) < 6, str(df.股票代码).zfill(6), df.股票代码)
    # print(df)
    df.to_sql(f'test_stock_{cur_y_m_d.replace("-", "_")}', con=init_engine(), index_label=['id'],
              if_exists='replace',
              dtype={
                  'id': types.BigInteger,
                  const.gpdm: types.VARCHAR(10),
                  const.gpmc: types.VARCHAR(10),
                  const.zxj: types.VARCHAR(10),
                  const.zsz: types.VARCHAR(20),
                  const.zsz_d: types.VARCHAR(20),
                  const.mgsy: types.VARCHAR(20),
                  const.zzc: types.VARCHAR(20),
                  const.zzc_d: types.VARCHAR(20),
                  const.zfz: types.VARCHAR(20),
                  const.zfz_d: types.VARCHAR(20),
                  const.gdqyhj: types.VARCHAR(20),
                  const.gdqyhj_d: types.VARCHAR(20),
                  const.jlrtb: types.VARCHAR(20),
                  const.ystbl: types.VARCHAR(20),
                  const.gsnzjz_jlr: types.VARCHAR(20),
                  const.gsnzjz_ys: types.VARCHAR(20),
              })


@async_able
def run_crawl():
    start = du.start_tm()
    print(f'basedir = {basedir} \n')

    par_ls = [
        # (const.type_name_5g, const.code_url_5g),
        # (const.type_name_bank, const.code_url_bank),
        # (const.type_name_broker, const.code_url_broker),
        # (const.type_name_car, const.code_url_car),
        # (const.type_name_charging, const.code_url_charging),
        # (const.type_name_eletric, const.code_url_eletric),
        # (const.type_name_environment, const.code_url_environment),
        # (const.type_name_food, const.code_url_food),
        (const.type_name_insure, const.code_url_insure),
        # (const.type_name_medical, const.code_url_medical),
        # (const.type_name_medicine, const.code_url_medicine),
        # (const.type_name_security, const.code_url_security),
        # (const.type_name_software, const.code_url_software),
    ]

    # with BrowserPool(6) as b_pool:
    #     for par in par_ls:
    #         code_crawl(par[0], par[1], b_pool)
    #         detail_crawl(par[0], b_pool)
    #         finance_crawl(par[0], b_pool)
    #         analysis_crawl(par[0], b_pool)

    mysql_crawl(par_ls)

    du.end_tm(start, 'RunCrawl 总耗时')


if __name__ == '__main__':
    run_crawl()
