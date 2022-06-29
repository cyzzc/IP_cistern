import threading
import time

import schedule

from copy_ip.conn import read_yaml
from copy_ip.other.log import log_ip
from copy_ip.write_file import get_random_ip


def file_null():
    """
    配合定时任务取消代理的添加，写入配置文件 ' '
    :return:
    """
    get_random_ip(" ")
    log_ip('取消代理的时间是：' + time.strftime('%Y-%m-%d %H:%M:%S %p %X'))


def schedule_ds(ti):
    """
    根据时间执行特定任务
    :param ti: 时间参数
    :return:
    """
    schedule.every().day.at(str(ti)).do(file_null)
    while True:
        schedule.run_pending()
        time.sleep(1)


def timed_thread():
    timing = read_yaml()['timing']
    threads = []
    # 如果没有设置定时关闭代理就不添加定时任务
    if len(timing) > 0:
        log_ip("定时任务开启成功，中间会取消代理")
        for i in timing:
            t = threading.Thread(target=schedule_ds, args=(str(i),))
            threads.append(t)
        for t in threads:
            t.start()
        # 不关闭多线程连接，这样就可以一直执行
        # for t in threads:
        #     t.join()
    else:
        log_ip("你没有设置定时任务，中间不会取消代理")
