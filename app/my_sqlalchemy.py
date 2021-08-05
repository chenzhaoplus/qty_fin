from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from timeit import default_timer

host = 'v81'
port = 3306
db = 'python_crawl'
user = 'root'
password = '123456'

g_mysql_url = 'mysql+pymysql://%s:%s@%s:%d/%s' % (user, password, host, port, db)

engine = create_engine(g_mysql_url)

Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40))
    remark = Column(String(1000), nullable=True)
    isBuy = Column(Integer, default=1)


Base.metadata.create_all(engine)  # 创建表

Session = sessionmaker(bind=engine)


class UsingAlchemy(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        """
        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        self._session = Session()

    def __enter__(self):
        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._session.commit()

        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f 秒' % (self._log_label, diff))

    @property
    def session(self):
        return self._session


# 测试获取一条记录
def check_it():
    session = Session()

    result = session.query(Product).first()
    if result is None:
        session.commit()
        return None

    session.commit()
    print('-- 得到记录: {0}'.format(result))

    session.close()


# 测试获取一条记录
def check_it_2():
    with UsingAlchemy() as ua:
        result = ua.session.query(Product).first()
        print('-- 得到记录: {0}'.format(result))


if __name__ == '__main__':
    check_it()
    check_it_2()
