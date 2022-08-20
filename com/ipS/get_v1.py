import re

import requests

from com.other.heade import get_user_agent
from com.other.log import login
from com.pysqlit.py3 import IPsql


def get_v1():
    try:
        sql = IPsql()
        reps = requests.get("https://www.proxy-list.download/api/v1/get?type=http", headers=get_user_agent(),
                            timeout=20, verify=False)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text

        # 正则表达式
        # 分别是IP，端口，类型，国家
        re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):')
        re_port = re.compile(r':(\d{2,6})')
        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)
        for v in range(len(http_ip)):
            sql.insert_data([http_ip[v] + ':' + http_port[v], http_ip[v], http_port[v]], 'filter')
    except Exception as e:
        login(
            "异常问题，com-->ipS-->get_v1.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
