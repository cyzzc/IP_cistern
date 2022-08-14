import re

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_scan():
    """
    不管什么类型都转换成http协议
    :return:
    """
    try:
        reps = requests.get("https://www.proxyscan.io/", headers=get_user_agent(), timeout=20)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text
        # 保存到文件
        # 正则表达式
        # 分别是IP，端口，类型，国家
        re_ip = re.compile(r'<th scope="row">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</th>')
        re_port = re.compile(r'<td>(\d{2,6})</td>')
        re_country = re.compile(r'<td><span class="flag-icon .*?"></span>\s*(.*?)\s*</td>', re.S)
        # re_type = re.compile(r'<td>\s*([A-Z4-5,</span>]+)\s*</td>', re.S)
        #
        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)
        http_country = re_country.findall(re1)
        # http_type = re_type.findall(re1)
        for i in range(len(http_ip)):
            # 不管什么类型都写入http协议
            # http_ip_type = {"http": "http", "Http": "http", "HTTP": "http", "https": "http", "Https": "http", "HTTPS": "http", "socks": "socks", "Socks": "socks", "SOCKS": "socks", "Socks4": "socks4", "socks4": "socks4",
            #                 "SOCKS4": "socks4", "socks5": "socks5", "Socks5": "socks5", "SOCKS5": "socks5"}
            insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), 'http',
                        http_country[i], 'filter')
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_scan.py: " + str(e))