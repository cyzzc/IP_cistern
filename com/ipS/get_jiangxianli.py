import re

import requests

from com.other.heade import get_user_agent
from com.other.log import login
from com.pysqlit.py3 import IPsql


def get_jxl():
    """
    取消了地理位置，全部定义为国内CN
    :return:
    """
    sql = IPsql()
    try:
        reps = requests.get("https://ip.jiangxianli.com/?page=1", headers=get_user_agent(), timeout=20, verify=False)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text

        # 正则表达式
        # 分别是IP，端口，类型，国家
        re_ip = re.compile(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>')
        re_port = re.compile(r'<td>(\d{2,6})</td>')
        # re_country = re.compile(r'&quot;country&quot;: &quot;(\w+)')
        re_type = re.compile(r'<td>([HTPSCOK45]{4,6})</td>')

        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)
        # http_country = re_country.findall(re1)
        http_type = re_type.findall(re1)
        for i in range(len(http_ip)):
            # 转成小写
            http_type[i] = http_type[i].lower()
            # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
            if http_type[i] == "https" or http_type[i] == "http":
                http_ip_type = {"http": "http", "https": "http", "socks": "socks", "socks4": "socks4",
                                "socks5": "socks5"}
                sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]]],
                                'filter')
    except Exception as e:
        login(
            "异常问题，com-->ipS-->get_jiangxianli.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
