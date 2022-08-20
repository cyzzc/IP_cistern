import re
import time

import requests

from com.other.heade import get_user_agent


from com.other.log import log_ip
from com.pysqlit.py3 import insert_data


def get_github():
    try:
        urllist = [
            "https://raw.iqiq.io/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.iqiq.io/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.iqiq.io/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
            "https://raw.iqiq.io/UptimerBot/proxy-list/main/proxies/http.txt",
            "https://raw.iqiq.io/UptimerBot/proxy-list/main/proxies_anonymous/http.txt",
            "https://raw.iqiq.io/saisuiu/uiu/main/cnfree.txt",
            "https://raw.iqiq.io/saisuiu/uiu/main/free.txt",
        ]
        for url in urllist:
            time.sleep(8)
            reps = requests.get(url,
                                headers=get_user_agent(), verify=False, timeout=20)
            # 设置编码
            reps.encoding = "utf-8"
            re1 = reps.text
            # 正则表达式
            # 分别是IP，端口，类型，国家
            re_ip = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            re_port = re.compile(r':(\d{2,6})')
            http_ip = re_ip.findall(re1)
            http_port = re_port.findall(re1)
            # print(http_ip)
            # print(http_port)
            # print(len(http_ip))
            # print(len(http_port))
            for i in range(len(http_ip)):
                http_ip_type = "https" if url.split('/')[-1] == "https.txt" else "http"
                # 创建字典，里面存放所有网络协议,原因https 不能使用,但是转换成http协议可以使用
                insert_data(http_ip[i] + ':' + http_port[i], http_ip[i], int(http_port[i]), http_ip_type,
                            "Github", 'filter')
                pass
    except Exception as e:
        log_ip("异常问题，com-->ipS-->get_github.py: " + f'<em style="color: rgb(255, 0, 0); font-weight: bolder">{str(e)}</em>')

