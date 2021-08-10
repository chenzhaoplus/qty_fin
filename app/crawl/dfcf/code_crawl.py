import time
from concurrent.futures import as_completed

import pandas as pd
from ..crawl import Crawl
from app.utils import file_utils, common_utils as cu

import app.utils.constants as const


class CodeCrawl(Crawl):

    def __init__(self, url, b_pool):
        super().__init__()
        self._url = url
        self._b_pool = b_pool

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def b_pool(self):
        return self._b_pool

    @b_pool.setter
    def b_pool(self, b_pool):
        self._b_pool = b_pool

    def get_url(self, b):
        b.get(self._url)
        # 隐性等待，最长等待时间30秒，只用设置一次
        # b.implicitly_wait(30)
        # 显性等待， condition 里的元素可见之后才会进行下步操作
        # condition = expected_conditions.visibility_of_element_located((By.ID, 'table_wrapper-table'))
        # WebDriverWait(driver=b, timeout=20, poll_frequency=0.5).until(condition)

    def parse_data(self, b, pn):
        print(f'分析数据第{pn}页')
        time.sleep(2)
        data = {
            const.gpdm[0]: [],
            const.gpmc[0]: [],
            const.zxj[0]: [],
            const.cjl_hand[0]: [],
            const.syl_dynamic[0]: [],
        }
        code_list = b.find_elements_by_xpath('//*[@id="table_wrapper-table"]/tbody/tr/td[2]')
        name_list = b.find_elements_by_xpath('//*[@id="table_wrapper-table"]/tbody/tr/td[3]')
        price_list = b.find_elements_by_xpath('//*[@id="table_wrapper-table"]/tbody/tr/td[5]')
        cjl_hand_list = b.find_elements_by_xpath('//*[@id="table_wrapper-table"]/tbody/tr/td[8]')
        syl_dy_list = b.find_elements_by_xpath('//*[@id="table_wrapper-table"]/tbody/tr/td[17]')
        for code in code_list:
            data[const.gpdm[0]].append(code.text)
        for name in name_list:
            data[const.gpmc[0]].append(name.text)
        for price in price_list:
            data[const.zxj[0]].append(price.text)
        for cjl in cjl_hand_list:
            data[const.cjl_hand[0]].append(cjl.text)
        for syl in syl_dy_list:
            data[const.syl_dynamic[0]].append(syl.text)
        print(f'分页数据第{pn}页, 分析后数据 = {data}')
        return data

    def store_data(self, f_name='res/股票基本信息.csv', data=None, by=const.gpdm[0], ascending=True):
        if data is None:
            raise ValueError("argument data cannot be null!")
        df = pd.DataFrame(data)
        df = df.sort_values(by=by, ascending=ascending, axis=0)
        df.to_csv(f_name, index=False)
        print(f'[最终文件数据], df = {df}')

    def run(self, b, pn):
        self.get_url(b)
        if pn > 0:
            a_btn = b.find_elements_by_css_selector('.paginate_page .paginate_button')[pn]
            a_btn.click()
        return self.parse_data(b, pn)

    def get_page_num(self):
        """
        获取页数pn
        :return: pn
        """
        b = self._b_pool.queue.get()
        self.get_url(b)
        pn_list = b.find_elements_by_css_selector('.paginate_page>a')
        pn = int(pn_list[-1].text) if pn_list and len(pn_list) > 0 else 1
        self._b_pool.queue.put(b)
        return pn

    def get_data_one_thread(self, pn):
        b = self._b_pool.queue.get()
        self.get_url(b)
        maps = init_maps()
        for i in range(pn):
            data = self.parse_data(b, i)
            concat_data(maps, data)
            a_btn = b.find_element_by_css_selector('.next')
            a_btn.click()
        self._b_pool.queue.put(b)
        return maps


def run(pn, crawl):
    b = crawl.b_pool.queue.get()
    data = crawl.run(b, pn)
    crawl.b_pool.queue.put(b)
    return data


def get_data_by_thread(pn, crawl):
    """
    多线程获取信息
    :return: data
    """
    all_task = []
    for i in range(pn):
        args = [i, crawl]
        future = crawl.b_pool.pool.submit(lambda p: run(*p), args)
        all_task.append(future)
    maps = init_maps()
    for future in as_completed(all_task):
        data = future.result()
        concat_data(maps, data)
    return maps


def concat_data(maps, data):
    maps[const.gpdm[0]] = maps[const.gpdm[0]] + data[const.gpdm[0]]
    maps[const.gpmc[0]] = maps[const.gpmc[0]] + data[const.gpmc[0]]
    maps[const.zxj[0]] = maps[const.zxj[0]] + data[const.zxj[0]]
    maps[const.cjl_hand[0]] = maps[const.cjl_hand[0]] + data[const.cjl_hand[0]]
    maps[const.syl_dynamic[0]] = maps[const.syl_dynamic[0]] + data[const.syl_dynamic[0]]


def init_maps():
    return {
        const.gpdm[0]: [],
        const.gpmc[0]: [],
        const.zxj[0]: [],
        const.cjl_hand[0]: [],
        const.syl_dynamic[0]: [],
    }


def begin_crawl(write_file, b_pool, url, type_name=''):
    crawl = CodeCrawl(url=url, b_pool=b_pool)
    cu.print_line(desc=f'{type_name}: 基本信息爬虫')
    file_utils.makedirs(write_file)
    pn = crawl.get_page_num()
    if pn <= 3:
        data = get_data_by_thread(pn, crawl)
    else:
        data = crawl.get_data_one_thread(pn)
    crawl.store_data(data=data, f_name=write_file)
    time.sleep(1)
