import time
from timeit import default_timer

from flask import current_app as cur_app


def get_cur_date(format_str='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format_str, time.localtime(time.time()))


def start_tm():
    # return datetime.datetime.now()
    return default_timer()


def end_tm(start_time=None, log_label='耗时'):
    # end_time = datetime.datetime.now()
    # log.log_info("total time: " + str((end_time - start_time).microseconds / 1000) + "ms")
    diff = default_timer() - start_time
    cur_app.logger.info('-- %s: %.6f 秒' % (log_label, diff))


if __name__ == '__main__':
    cur_app.logger.info(get_cur_date())
