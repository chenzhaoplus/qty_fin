import logging
import os
import time

cur_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
root_path = os.path.abspath(os.path.dirname(__file__)).split('shippingSchedule')[0]
if not os.path.exists(os.path.dirname(root_path + "\\logs\\")):
    os.makedirs(os.path.dirname(root_path + "\\logs\\"))
filename = f'{root_path}\\logs\\logging{cur_date}.log'

logging.basicConfig(
    level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    # filename=filename,  # log文件名
    filemode='w')  # 写入模式“w”或“a”

fh = logging.FileHandler(filename, encoding='UTF-8')
sh = logging.StreamHandler()

fh.setLevel(logging.INFO)  # 定义该handler级别
formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
fh.setFormatter(formatter)

logger = logging.getLogger('mylogger')
logger.propagate = False
logger.addHandler(fh)
logger.addHandler(sh)
