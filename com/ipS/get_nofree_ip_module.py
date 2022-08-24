import json
import re
import threading
import time

import requests

from com.interface.base import BaseData


class GetNoFreeIp(BaseData):
    def __init__(self):
        super().__init__()
        self.time_kill = []

    def time_kill_thread(self, _time):
        time.sleep(_time)
        self.time_kill.clear()

    def get_nofree(self, url=None):
        """
        返回txt 格式：
        27.153.5.211:22271
        只支持单个
        """
        try:
            if url:
                url = self.api_url
                if not self.api_url:
                    return -1
            time.sleep(0.8)
            reps = requests.get(url,
                                headers=self.user_agent, verify=False, timeout=20)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text
            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            re_port = re.compile(r':(\d{2,6})')
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            # print(http_ip)
            # print(http_port)
            # print(len(http_ip))
            # print(len(http_port))
            # self.add_filter_data(http_ip[i] + ':' + http_port[i],
            #                          [http_ip[i] + ':' + http_port[i], http_ip[i],
            #                           int(http_port[i]), _type, "Github"])
            second = self.ping(http_ip, unit='ms', timeout=10)
            if second and second < 1000.0:
                if not self.time_kill:
                    self.time_kill.append("{}://{}:{}".format("https", http_ip, http_port))
                    t = threading.Thread(target=self.time_kill_thread, args=(self, 180))
                    t.start()
                return self.time_kill[0]
            else:
                self.time_kill_thread(0.8)
                return -1

        except Exception as e:
            self.log_write(
                "异常问题，com-->ipS-->get_nofree.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
