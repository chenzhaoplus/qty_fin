from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.utils.date_utils as du
from app import db


class UsingAlchemy(object):

    def __init__(self, engine=None, commit=True, log_time=True, log_label='总用时'):
        """
        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        self._engine = engine if engine else db.engine
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def __enter__(self):
        # 如果需要记录时间
        if self._log_time is True:
            # self._start = default_timer()
            self._start = du.start_tm()

        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._session.commit()

        if self._log_time is True:
            # diff = default_timer() - self._start
            # logger.info('-- %s: %.6f 秒' % (self._log_label, diff))
            du.end_tm(self._start, self._log_label)

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine


def init_engine(host='v81', port=3306, db_name='python_crawl', user='root', pwd='123456'):
    url = 'mysql+pymysql://%s:%s@%s:%d/%s' % (user, pwd, host, port, db_name)
    return create_engine(url)
