import csv
import time
from concurrent.futures import as_completed
from queue import Queue

import pandas as pd
from logger_config import logger

import app.utils.constants as const
from app.utils import file_utils, common_utils as cu
from ..crawl import Crawl


class DetailCrawl(Crawl):

    def __init__(self, url, code, name, price, cjl_hand, syl_dy):
        """
        详细信息爬虫
        :param url:
        :param code: 股票代码
        :param name: 股票名称
        :param price: 最新价
        :param cjl_hand: 成交量-手
        :param syl_dy: 市盈率-动态
        """
        super().__init__()
        self._url = url
        self._code = code
        self._name = name
        self._price = price
        self._cjl_hand = cjl_hand
        self._syl_dy = syl_dy
        self._total_price = None  # 总市值
        self._mgsy = None  # 每股收益
        self._zzc = None  # 总资产
        self._zfz = None  # 总负债
        self._gdqyhj = None  # 股东权益合计
        self._jlrtb = None  # 净利润同比（%）
        self._ystbl = None  # 营收同比率（%）
        self._zys = None  # 总营收
        self._zlr = None  # 总利润
        self._jlr = None  # 净利润
        self._roe = None  # 净资产收益率-ROE

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
        mgsy = b.find_element_by_id('zxzb_mgsy')
        jlrtb = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[5]/td[2]')
        ystbl = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[6]/td[2]')
        total_price = b.find_elements_by_xpath('//*[@id="gt5"]')
        zzc = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[13]/td[2]')
        zfz = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[14]/td[2]')
        gdqyhj = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[15]/td[2]')
        zys = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[9]/td[2]')
        zlr = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[10]/td[2]')
        jlr = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[11]/td[2]')
        roe = b.find_elements_by_xpath('//*[@id="m_cwzy"]/tbody/tr[4]/td[2]')
        self._mgsy = mgsy.text
        self._jlrtb = jlrtb[0].text if jlrtb else ''
        self._ystbl = ystbl[0].text if ystbl else ''
        self._total_price = total_price[0].text if total_price else ''
        self._zzc = zzc[0].text if zzc else ''
        self._zfz = zfz[0].text if zfz else ''
        self._gdqyhj = gdqyhj[0].text if gdqyhj else ''
        self._zys = zys[0].text if zys else ''
        self._zlr = zlr[0].text if zlr else ''
        self._jlr = jlr[0].text if jlr else ''
        self._roe = roe[0].text if roe else ''
        logger.info(
            f'[详细数据], {const.gpdm[0]}={self._code}, {const.gpmc[0]}={self._name}, {const.zxj[0]}={self._price}, '
            f'{const.zsz[0]}={self._total_price}, {const.mgsy[0]}={self._mgsy}, '
            f'{const.jlrtb[0]}={self._jlrtb}, {const.ystbl[0]}={self._ystbl}')

    def store_data(self, f_name=None, data=None, by=None, ascending=False):
        pass

    def run(self, b):
        self.get_url(b)
        self.parse_data(b)
        return {
            const.gpdm[0]: self._code,
            const.gpmc[0]: self._name,
            const.zxj[0]: self._price,
            const.zsz[0]: self._total_price,
            const.mgsy[0]: self._mgsy,
            const.zzc[0]: self._zzc,
            const.zfz[0]: self._zfz,
            const.gdqyhj[0]: self._gdqyhj,
            const.jlrtb[0]: self._jlrtb,
            const.ystbl[0]: self._ystbl,
            const.zys[0]: self._zys,
            const.zlr[0]: self._zlr,
            const.jlr[0]: self._jlr,
            const.roe[0]: self._roe,
            const.cjl_hand[0]: self._cjl_hand,
            const.syl_dynamic[0]: self._syl_dy,
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
                url = f'http://data.eastmoney.com/stockdata/{line[0]}.html'
                crawl = DetailCrawl(url=url, code=line[0], name=line[1], price=line[2], cjl_hand=line[3],
                                    syl_dy=line[4])
                tasks.put(crawl)
    except FileNotFoundError:
        logger.error('无法打开文件')
    except LookupError:
        logger.error('指定了未知的编码!')
    except UnicodeDecodeError:
        logger.error('读取文件时解码错误!')
    return tasks


def store_data(f_name='res/股票详细信息.csv', data=None, by=const.mgsy[0], ascending=False):
    if data is None:
        raise ValueError("argument data cannot be null!")
    df = pd.DataFrame(data)
    df = df.sort_values(by=by, ascending=ascending, axis=0)
    df.to_csv(f_name, index=False)
    logger.info(f'[最终文件数据], df = {df}')


def begin_crawl(read_file, write_file, b_pool, type_name='', is_end=False):
    cu.print_line(desc=f'{type_name}: 详细信息爬虫')
    file_utils.makedirs(write_file)
    tasks = get_task_queue(read_file)
    data = get_data_by_thread(tasks, b_pool)
    store_data(data=data, f_name=write_file)
    time.sleep(1)
