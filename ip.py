from flask_apscheduler import APScheduler

from com.Web.index import run_web
from com.ipS.get_crape import get_crape
from com.ipS.get_ip3366 import get_ip3366
from com.ipS.get_jiangxianli import get_jxl
from com.ipS.get_kxdaili import get_kuai
from com.ipS.get_proxydb import get_proxydb
from com.ipS.get_proxylist import get_fate
from com.ipS.get_pzzqz import get_pzz
from com.ipS.get_scan import get_scan
from com.ipS.get_v1 import get_v1
from com.ipS.git_poxy import get_git_ip
from com.detect.http_re import check_ip
from com.ipS.ip_pool import get_ip
from com.other.conn import read_yaml
from com.other.country import country_revise
from com.other.log import log_ip
from com.pysqlit.py3 import select_data

scheduler = APScheduler()


def ip():
    """
    执行爬取
    :return:
    """
    area = read_yaml()
    # 获取代理
    get_ip()
    get_git_ip()
    get_fate()
    get_pzz()
    get_scan()
    get_kuai()
    get_ip3366()
    get_v1()
    get_jxl()
    get_proxydb()
    # 下面是适配非国内环境的代理
    if area['country'] != '国内':
        get_crape()
    # 测试代理
    check_ip()


@scheduler.task('interval', id='implement', hours=1)
def implement():
    """
    定时任务 每四小时检测一次大检测
    :return:
    """
    try:
        ip()
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
            ip()
        else:
            log_ip("数据长度大于6条，不需要重新爬取")
    else:
        log_ip("数据库中没有数据，重新爬取")
        ip()


if __name__ == '__main__':
    # 判断是否是国外环境以此来决定是否爬取国外代理池
    country_revise()
    #  timed_thread可能存在未知BUG，如果不取消代理请删除
    timing_ck()
    scheduler.start()
    run_web()
