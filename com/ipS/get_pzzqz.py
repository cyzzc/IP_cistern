import re

import requests

from com.other.heade import get_user_agent
from com.other.log import login
from com.pysqlit.py3 import IPsql




def get_pzz():
    try:
        sql = IPsql()
        reps = requests.get("https://pzzqz.com/", headers=get_user_agent(), timeout=20, verify=False)
        # 设置编码
        reps.encoding = "utf-8"
        re1 = reps.text
        # 保存到文件
        # 正则表达式
        # 分别是IP，端口，类型，国家
        re_ip = re.compile(r'<tr>\n?<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n?<td>')
        re_port = re.compile(r'</td>\n?<td>(\d{2,6})</td>\n?<td class="country">')
        re_country = re.compile(r'<span class=".*?"></span>\n?([A-Z].*?)\n?</td>\n?<td class="d-none d-sm-table-cell">')
        re_type = re.compile(r'</div>\n?</div>\n?</td>\n?<td>(\w+)</td>\n?<td class="d-none d-sm-table-cell">')
        #
        http_ip = re_ip.findall(re1)
        http_port = re_port.findall(re1)
        http_country = re_country.findall(re1)
        http_type = re_type.findall(re1)
        for i in range(len(http_ip)):
            # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
            if http_type[i] == "https" or http_type[i] == "http" or http_type[i] == "Https" or http_type[i] == "Http":
                http_ip_type = {"http": "http", "Http": "http", "https": "http", "Https": "http", "socks": "socks",
                                "Socks": "socks", "Socks4": "socks4", "socks4": "socks4",
                                "socks5": "socks5", "Socks5": "socks5"}
                sql.insert_data([http_ip[i] + ':' + http_port[i], http_ip[i], http_port[i], http_ip_type[http_type[i]],
                                 http_country[i]], 'filter')
    except Exception as e:
        login(
            "异常问题，com-->ipS-->get_pzzqz.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')
