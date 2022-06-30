import sqlite3

from com.other.conn import read_yaml


# 创建数据库方法
from com.other.log import log_ip


def create_db():
    """
    创建数据库
    :return:
    """
    try:
        # 创建数据库
        db = sqlite3.connect(read_yaml()["db"])
        # 创建游标
        cursor = db.cursor()
        return cursor, db
    except Exception as e:
        print("创建数据库失败" + str(e))
        return -1


# 创建表方法
def create_table():
    """
    创建表
    :return:
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 创建表 ip= 服务器ip port=端口 protocol=协议 country=国家，ip不能为空和唯一
        cursor.execute(
            "create table acting(ip_port varchar(20) primary key,ip varchar(15) not null,port int(6) not null,  protocol varchar(6), country varchar(10))")
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        print("创建表失败" + str(e))
        return -1


# 插入数据方法
def insert_data(ip_port, ip, port, protocol, country):
    """
    插入数据
    :param ip_port: ip:port
    :param ip: ip地址
    :param port: 端口
    :param protocol: 协议
    :param country: 地区
    :return:
    """
    db = None
    try:
        # 创建数据库
        cursor, db = create_db()
        # 插入数据 ip, port,  protocol, country
        cursor.execute("insert into acting values('%s','%s',%d,'%s','%s')" % (ip_port, ip, port, protocol, country))
        # cursor.execute("insert into ip values('%s',)" %)
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        log_ip("插入数据失败" + str(e))
        return -1


# 查询数据方法
def select_data(protocol=None):
    """
    查询数据所有
    :param protocol: 默认查询http和https,非None查询所有协议
    :return: http或https的代理
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 查询数据
        if protocol is None:
            # 查询协议是http或https到的内容
            cursor.execute("select * from acting where protocol='http' or protocol='https'")
        else:
            # 查询所有
            cursor.execute("select * from acting")
        # 获取数据
        data = cursor.fetchall()
        # 关闭数据库
        db.close()
        return data
    except Exception as e:
        print("查询失败" + str(e))
        return -1


# 删除所有数据方法
def delete_data():
    """
    删除数据
    :return:
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 删除数据
        cursor.execute('delete from acting')
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        print("删除失败" + str(e))
        return -1


# 删除某一条数据方法
def delete_one_data(ip_port):
    """
    删除数据
    :return: 正常返回0，不正常返回1
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 删除数据
        cursor.execute(f"delete from acting where ip_port='{ip_port}'")
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        print("删除失败" + str(e))
        return -1
