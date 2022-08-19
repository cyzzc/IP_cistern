import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import requests

from com.other.conn import read_yaml
from com.other.country import country_ip
from com.other.heade import get_user_agent
from com.pysqlit.py3 import select_data, delete_one_data, insert_data

AGlevel = read_yaml()["AGlevel"]
lock = threading.Lock()
pool = ThreadPoolExecutor(max_workers=200, thread_name_prefix="check_ip_")
all_task_list = []
getting_ip_flag = False
del_ip_list = []  # 怀疑列表（因网络波动造成误判，需二次确认才删除ip）


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
        check_wb = [
            "https://plogin.m.jd.com/",
            "https://api.m.jd.com/",
            "https://bean.m.jd.com",
            "http://isvjcloud.com",  # 基本只能是国内代理
        ]
        # 检测节点是否可用.多次检测，如果可用，就把节点添加到字典中，检测多个防止代理无效，主要用于京东使用代理验证京东网址是否支持代理
        # 请求超过3秒，就认为节点不可用
        # print(AGlevel)
        for i in range(0, AGlevel):
            requests.get(check_wb[i], proxies=proxies, headers=get_user_agent(), allow_redirects=False,
                         timeout=20, verify=False)
        if sql_name == 'filter':
            location = country_ip(proxies)
            lock.acquire()
            # 检测成功添加到可用代理的数据库中
            if location != -1:
                insert_data(data[0], data[1], data[2], data[3], location)
            # 删除节点筛选
            delete_one_data(ip_port, sql_name)
            lock.release()
        elif sql_name == 'acting':
            if http_ip_port in del_ip_list:
                # 如果正常了，那就不怀疑了XD
                del_ip_list.remove(http_ip_port)
    except Exception as e:
        # 不做任何输出,删除不可用的节点
        # print("kill-" + sql_name + '-' + http_ip_port)
        lock.acquire()
        if sql_name == 'acting':
            if http_ip_port in del_ip_list:
                delete_one_data(ip_port, sql_name)
                del_ip_list.remove(http_ip_port)
            else:
                del_ip_list.append(http_ip_port)
        elif sql_name == 'filter':
            delete_one_data(ip_port, sql_name)
        lock.release()


def check_ip(sql_name='filter'):
    """
    使用多线程检测代理IP的可用性
    :param sql_name:
    :return:
    """
    global all_task_list, getting_ip_flag
    if not getting_ip_flag:
        sq = select_data(sql_name)
        for i in sq:
            # t = threading.Thread(target=http_request, args=(i[3] + "://" + i[0], i[0], i, sql_name,))
            all_task_list.append(pool.submit(http_request, i[3] + "://" + i[0], i[0], i, sql_name))
        getting_ip_flag = True
        wait(all_task_list, return_when=ALL_COMPLETED)
        all_task_list = []
        getting_ip_flag = False
