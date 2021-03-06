import csv
import time
from concurrent.futures import as_completed
from queue import Queue

import pandas as pd
from logger_config import logger

from app.utils import constants as const, file_utils, common_utils as cu
from ..crawl import Crawl


class AnalysisCrawl(Crawl):

    def __init__(self, info, type_name=''):
        """
        信息分析爬虫
        :param code: 股票代码
        :param name: 股票名称
        :param price: 最新价
        """
        super().__init__()
        self._type_name = type_name
        self._code = info[0]
        self._name = info[1]
        self._price = info[2]
        self._total_price = info[3]  # 总市值
        self._total_price_d = cu.str_to_price(info[3])  # 总市值-数
        self._mgsy = info[4]  # 每股收益
        self._zzc = info[5]  # 总资产
        self._zzc_d = cu.str_to_price(info[5])  # 总资产-数
        self._zfz = info[6]  # 总负债
        self._zfz_d = cu.str_to_price(info[6])  # 总负债-数
        self._gdqyhj = info[7]  # 股东权益合计
        self._gdqyhj_d = cu.str_to_price(info[7])  # 股东权益合计-数
        self._jlrtb = cu.str_to_price(info[8])  # 净利润同比（%）
        self._ystbl = cu.str_to_price(info[9])  # 营收同比率（%）
        self._zys = info[10]  # 总营收
        self._zys_d = cu.str_to_price(info[10])  # 总营收-数
        self._zlr = info[11]  # 总利润
        self._zlr_d = cu.str_to_price(info[11])  # 总利润-数
        self._jlr = info[12]  # 净利润
        self._jlr_d = cu.str_to_price(info[12])  # 净利润-数
        self._roe = info[13]
        self._cjl_hand = info[14]  # 成交量-手
        self._syl_dy = info[15]  # 市盈率-动态
        self._ldbl = info[16]
        self._sdbl = info[17]
        self._gsnzjz_jlr = None  # 公司内在价值=(8.5+2*净利润增长率)*每股收益
        self._gsnzjz_ys = None  # 公司内在价值=(8.5+2*营收增长率)*每股收益

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    def get_url(self, b):
        pass

    def parse_data(self, b=None):
        try:
            self._gsnzjz_jlr = float((8.5 + 2 * float(self._jlrtb)) * float(self._mgsy)) if float(
                self._jlrtb) > 0 and float(self._mgsy) > 0 else None
            self._gsnzjz_jlr = round(self._gsnzjz_jlr, 2)
            self._gsnzjz_ys = float((8.5 + 2 * float(self._ystbl)) * float(self._mgsy)) if float(
                self._ystbl) > 0 and float(self._mgsy) > 0 else None
            self._gsnzjz_ys = round(self._gsnzjz_ys, 2)
        except Exception:
            self._gsnzjz_jlr = None
            self._gsnzjz_ys = None
        logger.info(
            f'[分析数据], {const.gpdm[0]}={self._code}, {const.gpmc[0]}={self._name}, {const.zxj[0]}={self._price}, '
            f'{const.zsz[0]}={self._total_price}, {const.mgsy[0]}={self._mgsy}, '
            f'{const.jlrtb[0]}={self._jlrtb}, {const.ystbl[0]}={self._ystbl}, '
            f'{const.gsnzjz_jlr[0]}={self._gsnzjz_jlr}, {const.gsnzjz_ys[0]}={self._gsnzjz_ys}')

    def store_data(self, f_name=None, data=None, by=None, ascending=False):
        pass

    def run(self, b=None):
        self.parse_data(b)
        return {
            'gpdm': self._code,
            const.gpmc[1]: self._name,
            const.gplx[1]: self._type_name,
            const.zxj[1]: self._price,
            const.zsz[1]: self._total_price,
            const.zsz_d[1]: self._total_price_d,
            const.mgsy[1]: self._mgsy,
            const.roe[1]: self._roe,
            const.cjl_hand[1]: self._cjl_hand,
            const.syl_dynamic[1]: self._syl_dy,
            const.zzc[1]: self._zzc,
            const.zzc_d[1]: self._zzc_d,
            const.zfz[1]: self._zfz,
            const.zfz_d[1]: self._zfz_d,
            const.gdqyhj[1]: self._gdqyhj,
            const.gdqyhj_d[1]: self._gdqyhj_d,
            const.jlrtb[1]: self._jlrtb,
            const.ystbl[1]: self._ystbl,
            const.zys[1]: self._zys,
            const.zys_d[1]: self._zys_d,
            const.zlr[1]: self._zlr,
            const.zlr_d[1]: self._zlr_d,
            const.jlr[1]: self._jlr,
            const.jlr_d[1]: self._jlr_d,
            const.ldbl[1]: self._ldbl,
            const.sdbl[1]: self._sdbl,
            const.gsnzjz_jlr[1]: self._gsnzjz_jlr,
            const.gsnzjz_ys[1]: self._gsnzjz_ys,
        }


def run(crawl, b_pool=None):
    data = crawl.run()
    return data


def get_data_by_thread(tasks, b_pool):
    futures = []
    while not tasks.empty():
        args = [tasks.get()]
        f = b_pool.pool.submit(lambda p: run(*p), args)
        futures.append(f)
    data = []
    for f in as_completed(futures):
        r = f.result()
        data.append(r)
    return data


def get_task_queue(read_file, type_name=''):
    try:
        tasks = Queue()
        with open(read_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rn = 0
            for line in reader:
                # if rn > 10:
                #     break
                rn += 1
                if rn == 1:
                    continue
                crawl = AnalysisCrawl(info=line, type_name=type_name)
                tasks.put(crawl)
    except FileNotFoundError:
        logger.error('无法打开文件')
    except LookupError:
        logger.error('指定了未知的编码!')
    except UnicodeDecodeError:
        logger.error('读取文件时解码错误!')
    return tasks


def store_data(f_name='res/股票分析信息.csv', data=None, by=const.gsnzjz_ys[1], ascending=False):
    if data is None:
        raise ValueError("argument data cannot be null!")
    df = pd.DataFrame(data)
    df.replace('-', '', inplace=True)
    df = df.sort_values(by=by, ascending=ascending, axis=0)
    df.to_csv(f_name, index=False)
    logger.info(f'[最终文件数据], df = {df}')


def begin_crawl(read_file, write_file, b_pool, by='公司内在价值-营收', type_name=''):
    cu.print_line(desc=f'{type_name}: 分析信息')
    file_utils.makedirs(write_file)
    tasks = get_task_queue(read_file, type_name=type_name)
    data = get_data_by_thread(tasks, b_pool)
    store_data(data=data, f_name=write_file, by=by)
    time.sleep(1)
