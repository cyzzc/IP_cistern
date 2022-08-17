import re

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_proxydb(area="CN"):
    try:
        reps = requests.get(f"http://proxydb.net/?country={area}", headers=get_user_agent(), timeout=20)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text
        # 保存到文件
        # 正则表达式
        re_ip = re.compile(r'<a href=.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):')
        re_port = re.compile(r':\d{2,6}</a>')
        re_country = re.compile(r'<abbr title=".*?">([A-Z].*?)\n?</abbr>')
        re_type = re.compile(r'\bHT\w+')
        #
        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)  # :80</a>
        http_country = re_country.findall(re1)
        http_type = re_type.findall(re1)
        if len(http_ip) < 3:
            return get_proxydb()
        for i in range(len(http_ip)):
            # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
            if http_type[i] == "https" or http_type[i] == "http" or http_type[i] == "Https" or http_type[i] == "Http":
                http_port[i] = http_port[i].replace("</a>", "")
                http_ip_type = {"http": "http", "Http": "http", "https": "http", "Https": "http", "socks": "socks",
                                "Socks": "socks", "Socks4": "socks4", "socks4": "socks4",
                                "socks5": "socks5", "Socks5": "socks5"}
                insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), http_ip_type[http_type[i]],
                            http_country[i], 'filter')
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_proxydb.py: " + str(e))
