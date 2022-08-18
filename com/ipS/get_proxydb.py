import re
import time

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_list():
    """
    获取这个代理池国家列表，爬取所有国家
    :return: 返回数组
    """
    try:
        print("正在获取代理池国家列表，爬取所有国家")
        country = requests.get("http://www.proxydb.net/", headers=get_user_agent(), timeout=20, verify=False)
        country.encoding = "utf-8"
        re1 = country.text
        re_country = re.compile(r'<option value="([A-Z]{2})">.*?\([1-9]\d*\)</option>')
        http_country = re_country.findall(re1)
        return http_country
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_proxydb.py-->get_list: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
        return []


def get_proxydb():
    """
    获取代理池的代理，爬取所有国家
    :return:
    """
    try:
        lists = get_list()
        for j in lists:
            time.sleep(5)
            print("正在获取代理池的代理，爬取所有国家")
            reps = requests.get(f"http://proxydb.net/?country={j}", headers=get_user_agent(), timeout=20, verify=False)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text
            # 保存到文件
            # 正则表达式
            re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):')
            re_port = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d{2,6})</a>')
            re_type = re.compile(r'<td>\s*([HTPSCOK45]{4,6})\s*</td>')
            #
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)  # :80</a>
            http_type = re_type.findall(re1)
            for i in range(len(http_ip)):
                # 把字母转换为小写
                http_type[i] = http_type[i].lower()
                if http_type[i] == "http" or http_type[i] == "https":
                    insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), http_type[i],
                                "SU", 'filter')
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_proxydb.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
