"""
请求后用于返回IP处理地方
"""
import random

import requests

from com.other.conn import read_yaml
from com.other.heade import get_user_agent
from com.other.log import log_ip
from com.pysqlit.py3 import delete_one_data, select_Location

data = read_yaml()


# 获取节点
def read_node():
    """
    随机IP，为了避免很多人同时使用一个IP
    :return: 返回协议://ip:端口，如果都不可用返回-1
    """
    sql = select_Location()
    randomnum = random.randint(0, len(sql) - 1)
    random_ip = sql[randomnum][3] + "://" + sql[randomnum][0]
    return random_ip


# 添加节点检测
def check_node():
    """
    添加之前再次检测节点是否可用
    获取随机节点
    :return: 返回协议://ip:端口 没有返回-1
    """
    sql = select_Location("中国")
    try:
        # 判断返回的是不是数组
        if isinstance(sql, list):
            # 判断数组长度是否大于3
            if len(sql) > 3:
                # 第一次使用随机IP，诺随机IP不可用，按顺序获取IP
                randomnum = random.randint(0, len(sql) - 1)
                random_ip = sql[randomnum][3] + "://" + sql[randomnum][0]
                return random_ip
        # 走到这里说明不复合上面的条件
        return read_node()
    except Exception as e:
        log_ip("节点池中没有节点代理池可能不能使用了，check_node：" + str(e))
        return -1
