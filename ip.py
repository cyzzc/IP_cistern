from flask_apscheduler import APScheduler

from com.Web.index import run_web
from com.ipS.git_poxy import get_git_ip
from com.detect.http_re import check_ip
from com.ipS.ip_pool import get_ip
from com.other.log import log_ip
from com.pysqlit.py3 import select_data

scheduler = APScheduler()


@scheduler.task('interval', id='implement', hours=3)
def implement():
    """
    定时任务 每四小时检测一次大检测
    :return:
    """
    try:
        # 获取代理
        get_ip()
        get_git_ip()
        # 测试代理
        check_ip()
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
            log_ip("数据长度小于6条，重新爬取")
            # 获取代理
            get_ip()
            get_git_ip()
            # 测试代理
            check_ip()
        else:
            log_ip("数据长度大于6条，不需要重新爬取")
    else:
        log_ip("数据库中没有数据，重新爬取")
        # 获取代理
        get_ip()
        get_git_ip()
        # 测试代理
        check_ip()


if __name__ == '__main__':
    #  timed_thread可能存在未知BUG，如果不取消代理请删除
    timing_ck()
    scheduler.start()
    run_web()
