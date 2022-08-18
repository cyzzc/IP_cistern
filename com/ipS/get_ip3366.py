import re

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_ip3366():
    try:
        for j in range(1, 10):
            try:
                reps = requests.get(f"https://proxy.ip3366.net/free/?action=china&page={j}", headers=get_user_agent(), timeout=20, verify=False)
                # 设置编码
                reps.encoding = "utf-8"
                re1 = reps.text

                # 正则表达式
                # 分别是IP，端口，类型，国家
                re_ip = re.compile(r'<td data-title="IP">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>')
                re_port = re.compile(r'<td data-title="PORT">(\d{2,6})</td>')
                http_ip = re_ip.findall(re1)
                http_port = re_port.findall(re1)
                for i in range(len(http_ip)):
                    insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), 'http',
                                "CN", 'filter')
            except Exception as e:
                return 0
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_ip3366.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')