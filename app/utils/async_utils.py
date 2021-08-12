from threading import Thread


# from time import sleep


def async_able(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

# @async_able
# def A():
#     sleep(10)
#     log.log_info("函数A睡了十秒钟。。。。。。")
#     log.log_info("a function")
#
#
# def B():
#     log.log_info("b function")
#
#
# A()
# B()
