import random
import threading
from queue import Queue

from com.other.conn import read_yaml
from com.other.log import login
from com.other.heade import get_user_agent
from com.pysqlit.py3 import IPsql
from ping3 import ping, verbose_ping


class BaseData:
    def __init__(self):
        self.sql = IPsql()
        self.log_write = login
        self.user_agent = get_user_agent()
        self.filter_data = dict()
        self.threadingLock = threading.Lock()
        self.ping = ping
        self.info_queue = Queue()
        self.pause_flag = False
        self.getting_ip_flag = False
        self.api_url = read_yaml()["IPAPI"]
        self.AGlevel = read_yaml()["AGlevel"]

    def clear_filter_data(self):
        self.filter_data.clear()

    def add_filter_data(self, k: str, v):
        # print(k, v)
        self.threadingLock.acquire()
        if len(v) == 3:
            # 直接抛出异常
            v[3] = "http"
        self.filter_data.setdefault(k, v)
        self.threadingLock.release()

    def del_filter_data(self, k):
        try:
            # print("删除:", k)
            self.threadingLock.acquire()
            if self.filter_data.get(k):
                self.filter_data.pop(k)
            self.threadingLock.release()
        except Exception as e:
            print("del_filter_data抛出异常-", e)
