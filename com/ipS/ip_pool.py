import json

import requests

from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_ip():
    """
    爬取的IP池地址
    :return:
    """
    # 获取网站数据
    url = 'https://uu-proxy.com/api/free'
    try:

        strhtml = requests.get(url, headers=get_user_agent(), verify=False)
        data = json.loads(strhtml.text)
        for i in range(len(data['free']['proxies'])):
            # 下面是 地址、端口号、协议、支持HTTPS
            ip = data['free']['proxies'][i]['ip']
            port = data['free']['proxies'][i]['port']
            protocol = data['free']['proxies'][i]['scheme']
            country = "CN"
            if protocol == "http" or protocol == "https":
                # 添加的数据库
                insert_data(ip + ':' + str(port), ip, port, protocol, country, 'filter')
        # 关闭爬取网站
        strhtml.close()

    except Exception as e:
        log_ip("异常提示,ip_pool>get_ip: " + str(e))
