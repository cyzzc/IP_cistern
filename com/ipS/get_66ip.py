import re

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_66ip():
    try:
        reps = requests.get("http://www.66ip.cn/", headers=get_user_agent(), timeout=20)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text
        # 保存到文件
        # 正则表达式
        re_ip = re.compile(r'<tr>\n?<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n?<td>')
        re_port = re.compile(r'</td>\n?<td>(\d{2,6})</td>\n?<td>')
        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)
        http_country = "中国"
        http_type = "http"
        for i in range(len(http_ip)):
            # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
            if http_type == "http":
                http_ip_type = {"http": "http", "Http": "http", "https": "http", "Https": "http", "socks": "socks",
                                "Socks": "socks", "Socks4": "socks4", "socks4": "socks4",
                                "socks5": "socks5", "Socks5": "socks5"}
                insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), http_ip_type[http_type],
                            http_country, 'filter')
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_66ip.py: " + str(e))
