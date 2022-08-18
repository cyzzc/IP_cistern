import sqlite3

from com.other.conn import read_yaml

# 创建数据库方法
from com.other.log import log_ip

db_path = read_yaml()["db"]

def create_db():
    """
    创建数据库
    :return:
    """
    try:
        # 创建数据库
        db = sqlite3.connect(db_path)
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
        return -1


def insert_data(ip_port, ip, port, protocol, country, surface='acting'):
    """
    插入数据
    :param ip_port: ip:port
    :param ip: ip地址
    :param port: 端口
    :param protocol: 协议
    :param country: 地区
    :param surface: 数据库表名，默认acting
    :return:
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 插入数据 ip, port,  protocol, country
        cursor.execute(
            f"insert into {surface} values('%s','%s','%d','%s','%s')" % (ip_port, ip, port, protocol, country))
        # cursor.execute("insert into ip values('%s',)" %)
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return -1


# 查询数据方法
def select_data(surface='acting'):
    """
    查询数据所有
    :param surface: 数据库表名，默认acting
    :return: http或https的代理
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 查询数据
        cursor.execute(f"select * from {surface}")
        # 获取数据
        data = cursor.fetchall()
        # 关闭数据库
        db.close()
        return data
    except Exception as e:
        log_ip("查询数据失败" + str(e))
        return -1


def select_Location(country=None, surface='acting'):
    """
    查询数据所有
    :param country: 国家
    :param surface: 数据库表名，默认acting
    :return: http或https的代理
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 查询数据
        if country is None:
            cursor.execute(f"select * from {surface}")
        else:
            # 查询某个国家的数据
            cursor.execute(f"select * from {surface} where country='{country}'")
        # 获取数据
        data = cursor.fetchall()
        # 关闭数据库
        db.close()
        return data
    except Exception as e:
        log_ip("查询数据失败" + str(e))
        return -1


# 删除所有数据方法
def delete_data(surface='acting'):
    """
    删除数据
    :param surface: 数据库表名，默认acting
    :return:
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 删除数据
        cursor.execute(f'delete from {surface}')
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return -1


# 删除某一条数据方法
def delete_one_data(ip_port, surface='acting'):
    """
    删除数据
    :param ip_port: ip:port
    :param surface: 数据库表名，默认acting
    :return: 正常返回0，不正常返回1
    """
    try:
        # 创建数据库
        cursor, db = create_db()
        # 删除数据
        cursor.execute(f"delete from {surface} where ip_port='{ip_port}'")
        db.commit()
        # 关闭数据库
        db.close()
        return 0
    except Exception as e:
        return -1
