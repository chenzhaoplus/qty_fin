from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from logger_config import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BrowserPool:

    def __init__(self, concurrency=5, init_browser=True):
        self._queue = Queue(concurrency)
        self._pool = ThreadPoolExecutor(concurrency)
        self._init_browser = init_browser
        self._concurrency = concurrency

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, queue):
        self._queue = queue

    @property
    def pool(self):
        return self._pool

    @pool.setter
    def pool(self, pool):
        self._pool = pool

    # def submit(self, *args, **kwargs):
    #     return self._pool.submit(args, kwargs)

    def __enter__(self):
        if self._init_browser:
            for i in range(self._concurrency):
                self._pool.submit(self.put_queue, (i + 1))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pool.shutdown(wait=True)
        bc = 1
        while not self._queue.empty():
            self._queue.get().quit()
            logger.info(f'关闭浏览器{bc}')
            bc += 1

    def put_queue(self, bc):
        logger.info(f'开启浏览器{bc}')
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 不显示浏览器启动及执行过程
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        chrome_options.add_argument(f'User-Agent={UserAgent}')
        driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
        self._queue.put(driver)
