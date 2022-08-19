import threading
import time

from flask_apscheduler import APScheduler
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from com.Web.index import run_web
from com.ipS.get_crape import get_crape
from com.ipS.get_ip3366 import get_ip3366
from com.ipS.get_jiangxianli import get_jxl
from com.ipS.get_kxdaili import get_kuai
from com.ipS.get_proxydb import get_proxydb
from com.ipS.get_proxylist import get_fate
from com.ipS.get_proxynova import get_proxynova
from com.ipS.get_pzzqz import get_pzz
from com.ipS.get_scan import get_scan
from com.ipS.get_v1 import get_v1
from com.ipS.git_poxy import get_git_ip
from com.detect.http_re import check_ip
from com.ipS.ip_pool import get_uu_proxy
from com.other.conn import read_yaml
from com.other.country import country_revise, aglevel
from com.other.log import log_ip
from com.pysqlit.py3 import select_data

scheduler = APScheduler()
pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="get_ip_")
lock = threading.Lock()
all_task_list = []
getting_ip_flag = False


def get_ip():
    """
    执行爬取
    :return:
    """
    global all_task_list, getting_ip_flag
    if getting_ip_flag:
        return
    area = read_yaml()
    all_task_list = []
    # 获取代理
    ip_db = {
        "get_ip": get_uu_proxy,
        "get_git_ip": get_git_ip,
        "get_fate": get_fate,
        "get_pzz": get_pzz,
        "get_scan": get_scan,
        "get_kuai": get_kuai,
        "get_ip3366": get_ip3366,
        "get_v1": get_v1,
        "get_jxl": get_jxl,
        "get_proxydb": get_proxydb,
        "get_proxynova": get_proxynova,  # 不能使用去方法里面查看异常信息
        "get_crape": get_crape  # 适配非国内环境的代理
    }
    for task in ip_db.keys():
        not_included = ["get_crape"]
        # 本身携带异步且有handle的，丢进线程池会有bug
        not_in_pool = ["get_proxynova"]
        if task not in not_included and task not in not_in_pool:
            # print("任务提交:" + task)
            all_task_list.append(pool.submit(ip_db.get(task)))
        if task in not_in_pool:
            # print("任务执行:" + task)
            ip_db.get(task)()

    # 下面是适配非国内环境的代理
    if area['country'] != '国内':
        all_task_list.append(pool.submit(ip_db.get("get_crape")))
    log_ip("开始爬取ip")
    getting_ip_flag = True
    # wait(all_task_list, return_when=ALL_COMPLETED)
    # 测试代理
    # check_ip()


def check_all_task_list_thread():
    """
    监听线程池任务线程，防止重复提交到任务池
    """
    global all_task_list, getting_ip_flag
    wait(all_task_list, return_when=ALL_COMPLETED)
    log_ip("爬取ip完毕")
    getting_ip_flag = False


def check_add_ip_thread():
    """
    监听添加线程
    """
    log_ip("监听筛选池线程启动成功")
    count = 1
    while True:
        time.sleep(count)
        sql = select_data(surface='filter')
        if type(sql) == list:
            if len(sql) >= 5:
                lock.acquire()
                check_ip()
                count = 1
                lock.release()
        else:
            if count < 15:
                count = +2


def check_exist_ip_thread():
    """
    监听ip存活线程
    """
    log_ip("监听ip池存活线程启动成功")
    while True:
        time.sleep(35)
        sql = select_data(surface='acting')
        if type(sql) == list:
            if len(sql) >= 0:
                lock.acquire()
                check_ip("acting")
                lock.release()


@scheduler.task('interval', id='conn_random', days=1)
def conn_random():
    """
    AGleve随机数
    :return:
    """
    aglevel()


@scheduler.task('interval', id='implement', hours=1)
def implement():
    """
    定时任务 每四小时检测一次大检测
    :return:
    """
    try:
        get_ip()
    except Exception as e:
        log_ip("定时任务报错" + str(e))


@scheduler.task('interval', id='timing_ck', minutes=2)
def timing_ck():
    """
    定时任务 每⑤分钟检测一次
    :return:
    """
    # 用来获取数据长度
    sql = select_data()
    # 检测返回的类型
    if type(sql) == list:
        # 如果数据长度不大于6条，就重新爬取
        if len(sql) <= 5:
            get_ip()
        else:
            log_ip(
                f'ip数据还有<b style="color: rgb(255, 0, 255); font-weight: bolder">{len(sql)}条</b>, 不需要重新爬取')
    else:
        log_ip("数据库中没有数据，重新爬取")
        get_ip()


if __name__ == '__main__':
    log_ip('<h1 style="color: rgb(111, 255, 0);">===程序开始运行===</h1>')
    # 判断是否是国外环境以此来决定是否爬取国外代理池
    country_revise()
    #  timed_thread可能存在未知BUG，如果不取消代理请删除
    timing_ck()
    scheduler.start()
    t1 = threading.Thread(target=check_add_ip_thread)
    t2 = threading.Thread(target=check_exist_ip_thread)
    t3 = threading.Thread(target=check_all_task_list_thread)
    t1.start()
    t2.start()
    t3.start()
    run_web()
