import re
import time

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_66ip():
    """
    网址测试时候503，暂时留着，等后面复活后使用
    :return:
    """
    try:
        time.sleep(3)
        reps = requests.get("http://www.66ip.cn/", headers=get_user_agent(), timeout=20, verify=False)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text
        # 保存到文件
        # 正则表达式
        re_ip = re.compile(r'<tr>\n?<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n?<td>')
        re_port = re.compile(r'</td>\n?<td>(\d{2,6})</td>\n?<td>')
        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)
        # print(http_ip)
        # print(http_port)
        # print(len(http_ip))
        # print(len(http_port))
        for i in range(len(http_ip)):
            insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), "http",
                        "CN", 'filter')
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_66ip.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
