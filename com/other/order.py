import time

from com.interface.base import BaseData
from com.other.conn import revise_yaml, read_yaml


class Order(BaseData):
    def __init__(self):
        super().__init__()

    def re_get_ip(self):
        """
        暂时用不上
        """
        if self.getting_ip_flag:
            return -1
        else:
            self.getting_ip_flag = False

    def pause_check_node(self):
        # print(self.pause_flag)
        self.pause_flag = True
        # print(self.pause_flag)

    def continue_check_node(self):
        self.pause_flag = False

    def get_all_acting_ip(self):
        return self.sql.select_data()

    def revise_api(self, _url):
        revise_yaml(f"IPAPI: {_url}", self.read()['Label']['IPAPI'])

    def revise_AGlevel(self, _grade: int):
        revise_yaml(f"AGlevel: {_grade}", self.read()['Label']['AGlevel'])

    def get_AGlevel(self):
        return self.read()["AGlevel"]

    def flash_all_yaml(self):
        self.flash_AGlevel()
        self.flash_api_url()
