import logging
import os
import time

from com.other.conn import read_yaml, read_txt

path = read_yaml()['log']
# 1.创建日志器对象
logger = logging.getLogger()
# 2.创建处理器(控制台)
file_handle = logging.FileHandler(path, mode='a', encoding="utf-8")
# 控制台的等级
file_handle.setLevel(level="ERROR")
logger.addHandler(file_handle)


def log_ip(data):
    aa = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logger.error(f"{aa} : {data}")
    file_handle.close()
    dele_ip()


def dele_ip():
    # 当文件大于3M时，删除文件
    if os.path.getsize(path) > 3242880:
        os.remove(path)


def rz():
    """
    读取日志文件
    :return: 打印html格式的日志，异常返回-1
    """
    try:
        sun = ''
        yml = read_yaml()
        if yml == -1:
            return -1
        rz1 = read_txt(yml['log'])
        if rz1 == -1:
            return -1
        # 遍历所有行
        for i in rz1:
            # 如果就\n则跳过
            if i == '\n':
                continue
            #  把末尾的\n换成<br>
            j = i.replace('\n', '<br>')
            sun += j
        return sun
    except Exception as e:
        return -1
