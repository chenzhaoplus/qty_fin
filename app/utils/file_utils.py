import os


def makedirs(path):
    """
    如果目录不存在，添加文件路径下的所有目录
    :param path:
    :return:
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))


if __name__ == '__main__':
    pass
