import csv
import time
from concurrent.futures import as_completed
from queue import Queue

import pandas as pd

import app.utils.constants as const
from ..crawl import Crawl
from app.utils import file_utils, common_utils as cu


class FinanceCrawl(Crawl):

    def __init__(self, url, info):
        """
        财务信息爬虫
        :param url:
        :param code: 股票代码
        :param name: 股票名称
        :param price: 最新价
        :param cjl_hand: 成交量-手
        :param syl_dy: 市盈率-动态
        """
        super().__init__()
        self._url = url
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
        self._jlrtb = info[8]  # 净利润同比（%）
        self._ystbl = info[9]  # 营收同比率（%）
        self._zys = info[10]  # 总营收
        self._zys_d = cu.str_to_price(info[10])  # 总营收-数
        self._zlr = info[11]  # 总利润
        self._zlr_d = cu.str_to_price(info[11])  # 总利润-数
        self._jlr = info[12]  # 净利润
        self._jlr_d = cu.str_to_price(info[12])  # 净利润-数
        self._roe = info[13]
        self._cjl_hand = info[14]  # 成交量-手
        self._syl_dy = info[15]  # 市盈率-动态
        self._ldbl = None  # 流动比率
        self._sdbl = None  # 速动比率

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

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
        b.get(self._url)
        # 隐性等待，最长等待时间30秒，只用设置一次
        # b.implicitly_wait(30)
        # 显性等待， condition 里的元素可见之后才会进行下步操作
        # condition = expected_conditions.visibility_of_element_located((By.ID, 'table_wrapper-table'))
        # WebDriverWait(driver=b, timeout=20, poll_frequency=0.5).until(condition)

    def parse_data(self, b):
        time.sleep(1)
        ldbl = b.find_elements_by_xpath(f'//span[text()="{const.ldbl}"]/parent::td/following-sibling::td[1]/span')
        sdbl = b.find_elements_by_xpath(f'//span[text()="{const.sdbl}"]/parent::td/following-sibling::td[1]/span')
        self._ldbl = ldbl[0].text if ldbl else ''
        self._sdbl = sdbl[0].text if sdbl else ''
        print(
            f'[财务数据], {const.gpdm}={self._code}, {const.gpmc}={self._name}, {const.zxj}={self._price}, '
            f'{const.zsz}={self._total_price}, {const.mgsy}={self._mgsy}, '
            f'{const.jlrtb}={self._jlrtb}, {const.ystbl}={self._ystbl}')

    def store_data(self, f_name=None, data=None, by=None, ascending=False):
        pass

    def run(self, b):
        self.get_url(b)
        self.parse_data(b)
        return {
            const.gpdm: self._code,
            const.gpmc: self._name,
            const.zxj: self._price,
            const.zsz: self._total_price,
            const.mgsy: self._mgsy,
            const.zzc: self._zzc,
            const.zfz: self._zfz,
            const.gdqyhj: self._gdqyhj,
            const.jlrtb: self._jlrtb,
            const.ystbl: self._ystbl,
            const.zys: self._zys,
            const.zlr: self._zlr,
            const.jlr: self._jlr,
            const.roe: self._roe,
            const.cjl_hand: self._cjl_hand,
            const.syl_dynamic: self._syl_dy,
            const.ldbl: self._ldbl,
            const.sdbl: self._sdbl,
        }


def run(crawl, b_pool):
    b = b_pool.queue.get()
    data = crawl.run(b)
    b_pool.queue.put(b)
    return data


def get_data_by_thread(tasks, b_pool):
    futures = []
    while not tasks.empty():
        args = [tasks.get(), b_pool]
        f = b_pool.pool.submit(lambda p: run(*p), args)
        futures.append(f)
    data = []
    for f in as_completed(futures):
        r = f.result()
        data.append(r)
    return data


def get_task_queue(read_file):
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
                url = f'http://emweb.securities.eastmoney.com/FinanceAnalysis/Index?type=web&code={cu.which_trade(line[0])}'
                crawl = FinanceCrawl(url=url, info=line)
                tasks.put(crawl)
    except FileNotFoundError:
        print('无法打开文件')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    return tasks


def store_data(f_name='res/股票财务信息.csv', data=None, by='每股收益', ascending=False):
    if data is None:
        raise ValueError("argument data cannot be null!")
    df = pd.DataFrame(data)
    df = df.sort_values(by=by, ascending=ascending, axis=0)
    df.to_csv(f_name, index=False)
    print(f'[最终文件数据], df = {df}')


def begin_crawl(read_file, write_file, b_pool, type_name=''):
    cu.print_line(desc=f'{type_name}: 财务信息爬虫')
    file_utils.makedirs(write_file)
    tasks = get_task_queue(read_file)
    data = get_data_by_thread(tasks, b_pool)
    store_data(data=data, f_name=write_file)
    time.sleep(1)
