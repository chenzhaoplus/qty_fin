from abc import ABCMeta, abstractmethod


class Crawl(object, metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def parse_data(self):
        pass

    @abstractmethod
    def store_data(self, f_name=None, data=None, by=None, ascending=False):
        pass

    @abstractmethod
    def run(self, b):
        pass
