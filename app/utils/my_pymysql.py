from timeit import default_timer

import pymysql
from dbutils.pooled_db import PooledDB
from flask import current_app
from logger_config import logger


class DMysqlConfig:
    """
        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host:数据库ip地址
        :param port:数据库端口
        :param db:库名
        :param user:用户名
        :param passwd:密码
        :param charset:字符编码
    """

    def __init__(self, host, db, user, password, port=3306):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password

        self.charset = 'UTF8'  # 不能是 utf-8
        self.minCached = 10
        self.maxCached = 20
        self.maxShared = 10
        self.maxConnection = 100

        self.blocking = True
        self.maxUsage = 0
        self.setSession = None
        self.reset = True


# ---- 用连接池来返回数据库连接
class DMysqlPoolConn:
    __pool = None

    def __init__(self, config):
        if not self.__pool:
            self.__class__.__pool = PooledDB(creator=pymysql,
                                             maxconnections=config.maxConnection,
                                             mincached=config.minCached,
                                             maxcached=config.maxCached,
                                             maxshared=config.maxShared,
                                             blocking=config.blocking,
                                             maxusage=config.maxUsage,
                                             setsession=config.setSession,
                                             charset=config.charset,
                                             host=config.host,
                                             port=config.port,
                                             database=config.db,
                                             user=config.user,
                                             password=config.password,
                                             )

    def get_conn(self):
        return self.__pool.connection()


# ========== 在程序的开始初始化一个连接池
# host = 'v81'
# port = 3306
# db = 'python_crawl'
# user = 'root'
# password = '123456'
# db_config = DMysqlConfig(host, db, user, password, port)
# config = current_app.config
# db_config = DMysqlConfig(config.get("DB_HOST"), config.get("DB_PORT"), config.get("DB_USER"), config.get("DB_PWD"),
#                          config.get("DB_PORT"))

# g_pool_connection = DMysqlPoolConn(db_config)


# ---- 使用 with 的方式来优化代码
class UsingMysql(object):

    def __init__(self, db_config=None, commit=True, log_time=True, log_label='总用时'):
        """
        :param commit: 是否在最后提交事务(设置为False的时候方便单元测试)
        :param log_time:  是否打印程序运行总时间
        :param log_label:  自定义log的文字
        """
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        db_config = db_config if db_config else current_app.config.get("DB_CONFIG")
        self._g_pool_connection = DMysqlPoolConn(db_config)

    def __enter__(self):
        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 从连接池获取数据库连接
        conn = self._g_pool_connection.get_conn()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()

        if self._log_time is True:
            diff = default_timer() - self._start
            logger.info('-- %s: %.6f 秒' % (self._log_label, diff))

    # ========= 一系列封装的业务方法

    # 返回 count
    def get_count(self, sql, params=None, count_key='count(id)'):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchone()
        if not data:
            return 0
        return data[count_key]

    def fetch_one(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def fetch_by_pk(self, sql, pk):
        self.cursor.execute(sql, (pk,))
        return self.cursor.fetchall()

    def update_by_pk(self, sql, params=None):
        self.cursor.execute(sql, params)

    @property
    def cursor(self):
        return self._cursor

    @property
    def conn(self):
        return self._conn


def init_dbconfig(db_host='v81', db_port=3306, db_name='python_crawl', db_user='root', db_pwd='123456'):
    return DMysqlConfig(db_host, db_name, db_user, db_pwd, db_port)
