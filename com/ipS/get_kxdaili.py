import re

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_kuai():
    try:
        for i in range(1, 3):
            for j in range(1, 11):
                try:
                    reps = requests.get(f"http://www.kxdaili.com/dailiip/{i}/{j}.html", headers=get_user_agent(), timeout=20, verify=False)
                    # 设置编码
                    reps.encoding = "utf-8"
                    re1 = reps.text
                    # 正则表达式
                    # 分别是IP，端口，类型，国家
                    re_ip = re.compile(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>')
                    re_port = re.compile(r'<td>(\d{2,6})</td>')

                    http_ip = re_ip.findall(re1)
                    http_port = re_port.findall(re1)
                    for v in range(len(http_ip)):
                        insert_data(http_ip[v] + ':' + http_port[v], http_ip[v], int(http_port[v]), 'http',
                                    'CN', 'filter')
                except Exception as e:
                    return 0
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_kxdaili.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
