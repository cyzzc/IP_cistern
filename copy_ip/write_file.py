# 写入文件
import random

import requests

from copy_ip.conn import read_yaml
from copy_ip.other.heade import get_user_agent
from copy_ip.other.log import log_ip
from copy_ip.pysqlit.py3 import select_data

data = read_yaml()


def get_random_ip(random_ip):
    """
    如果节点都不可以用，就把写入文件空，让ql使用主机IP，
    添加路径异常判断，如果路径不存在，打印路径不存在
    :return:
    """
    log_ip("本次IP是" + str(random_ip))
    # 判断 路径和行是否都添加 与 长度不等于0
    sum_path = len(data['path'])
    if sum_path == len(data['line']) and sum_path > 0:
        # 循环数组，添加多个文本
        for i in range(sum_path):
            # 写入文件
            try:
                f = open(data['path'][i], 'r+', encoding='utf-8')
                flist = f.readlines()
                # ql行数从一开始，python读取从零开始
                try:
                    flist[int(data['line'][i]) - 1] = '{}\n'.format(random_ip)
                    log_ip("写入文件成功,添加代理是: " + str(random_ip))
                    f = open(data['path'][i], 'w+', encoding='utf-8')
                    f.writelines(flist)
                except Exception as e:
                    log_ip("可能行不存在异常问题，get_random_ip：" + str(e))
                    print("可能行不存在异常问题，get_random_ip：" + str(e))
                f.close()
            except Exception as e:
                # 打印明显异常信息
                log_ip("可能路径不存在，get_random_ip：" + str(e))
                print("可能路径不存在，get_random_ip：" + str(e))
    else:
        log_ip("请检查conn.yml文件的路径和行是否一一对应，get_random_ip")
        print("请检查conn.yml文件的路径和行是否一一对应，get_random_ip")


# 获取节点
def read_node():
    sql = select_data()
    for i in range(len(sql)):
        random_ip = sql[i][3] + "://" + sql[i][0]
        proxies = {
            'http': random_ip,
            'https': random_ip
        }

        try:
            s = requests.session()
            s.keep_alive = False
            output1 = requests.get("https://baidu.com/", proxies=proxies, headers=get_user_agent(), timeout=2,
                                   verify=False)
            if output1.status_code == 200:
                output1.close()
                get_random_ip('export ALL_PROXY=' + random_ip)
                print("节点可用，添加代理是：" + str(random_ip))
                return 0
        except Exception as e:
            print("节点不可用，节点是：" + str(e))
            pass
    # 所有节点都不可用,删除节点那以后文字
    log_ip("所有节点都不可用,删除添加行文字")
    print("所有节点都不可用,删除添加行文字")
    get_random_ip("# ")


# 添加节点检测
def check_node():
    """
    添加之前再次检测节点是否可用
    获取随机节点
    :return:
    """
    sql = select_data()
    try:
        # 第一次使用随机IP，诺随机IP不可用，按顺序获取IP
        random_ip = random.randint(0, len(sql) - 1)
        print(random_ip)
        random_ip = sql[random_ip][3] + "://" + sql[random_ip][0]
        proxies = {
            'http': random_ip,
            'https': random_ip
        }
        try:
            output1 = requests.get("https://plogin.m.jd.com/", proxies=proxies, headers=get_user_agent(), timeout=2,
                                   verify=False)
            if output1.status_code == 200:
                output1.close()
                print("随机，节点可用，添加代理是：" + str(random_ip))
                get_random_ip('export ALL_PROXY=' + random_ip)
            # 添加节点成功
        except Exception as e:
            print("随机，节点不可用，节点是：" + str(e))
            read_node()
    except Exception as e:
        log_ip("节点池中没有节点代理池可能不能使用了，check_node：" + str(e))
        print("节点池中没有节点代理池可能不能使用了，异常：" + str(e))
        read_node()
