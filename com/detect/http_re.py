import threading

import requests

from com.other.country import country_ip
from com.other.heade import get_user_agent
from com.pysqlit.py3 import select_data, delete_one_data, insert_data

lock = threading.Lock()


def http_request(http_ip_port, ip_port, data, sql_name='filter'):
    """
    检测节点是否可用
    :param data:
    :param http_ip_port: 测试的节点
    :param ip_port: 如果不可用删除的索引
    :param sql_name: 扫描的数据库
    :return:
    """
    proxies = {
        'http': http_ip_port,
        'https': http_ip_port
    }
    try:
        # 检测节点是否可用.多次检测，如果可用，就把节点添加到字典中，检测多个防止代理无效，主要用于京东使用代理验证京东网址是否支持代理
        # 请求超过3秒，就认为节点不可用
        requests.get("https://plogin.m.jd.com/", proxies=proxies, headers=get_user_agent(), timeout=10).close()
        location = country_ip(proxies)
        lock.acquire()
        # 检测成功添加到可用代理的数据库中
        if location != -1 and sql_name == 'filter':
            insert_data(data[0], data[1], data[2], data[3], location)
        # 删除节点筛选
        delete_one_data(ip_port, sql_name)
        lock.release()
    except Exception as e:
        # 不做任何输出,删除不可用的节点
        lock.acquire()
        delete_one_data(ip_port, sql_name)
        lock.release()


# 使用多线程检测代理IP的可用性
def check_ip(sql_name='filter'):
    sq = select_data(sql_name)
    threads = []
    for i in sq:
        t = threading.Thread(target=http_request, args=(i[3] + "://" + i[0], i[0], i,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
