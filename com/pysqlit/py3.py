# -*- coding:utf8 -*-
import sqlite3

from com.other.conn import read_yaml

db_path = read_yaml()["db"]


class IPsql:

    def __init__(self):
        self.conn = sqlite3.connect(db_path, timeout=10)
        self.cursor = self.conn.cursor()

    def create_table(self) -> int:
        """
        创建表
        :return: 成0反-1
        """
        try:
            # 创建表 ip= 服务器ip port=端口 protocol=协议 country=国家，ip不能为空和唯一
            sql = "create table acting(ip_port varchar(20) primary key,ip varchar(15) not null,port int(6) not null,  " \
                  "protocol varchar(6), country varchar(10)) "
            self.cursor.execute(sql)
            self.conn.commit()
            return 0
        except Exception as e:
            return -1

    def insert_data(self, data: list, table_name='acting') -> int:
        """
        插入数据，根据传入的数据类型进行判断，自动选者插入方式
        :param data: 要插入的数据 [ip:port,ip地址,端口,协议,地区],其中协议和地区可以不带
        :param table_name: 表名,默认acting
        :return: 0 or -1
        """
        global sql
        try:
            if isinstance(data, list):
                # 获取data长度
                long = len(data)
                lis = ['http', 'No']
                # 表示插入值完整不用补充
                if long > 4:
                    sql = f"INSERT INTO {table_name} VALUES ('{data[0]}','{data[1]}',{data[2]},'{data[3]}','{data[4]}')"
                elif long == 4:
                    sql = f"INSERT INTO {table_name} VALUES ('{data[0]}','{data[1]}',{data[2]},'{data[3]}', '{lis[1]}')"
                elif long == 3:
                    sql = f"INSERT INTO {table_name} VALUES ('{data[0]}','{data[1]}',{data[2]}, '{lis[0]}', '{lis[1]}')"
                self.cursor.execute(sql)
            return 0
        except Exception as e:
            return -1
        finally:
            self.conn.commit()

    def select_data(self, country="Null", surface='acting') -> list:
        """
        查询数据所有
        :param country: 国家, 默认所有
        :param surface: 数据库表名，默认acting
        :return: http或https的代理,反之-1
        """
        try:
            if country != "Null":
                self.cursor.execute(f"select * from {surface} where country='{country}'")
            else:
                self.cursor.execute(f"select * from {surface}")
            # 获取查询数据
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            return []

    def delete_data(self, ip_port, surface='acting') -> int:
        """
        根据条件删除数据
        :param ip_port: ip:port
        :param surface: 数据库表名，默认acting
        :return: 正常返回0，不正常返回1
        """
        try:
            self.conn.execute(f"delete from {surface} where ip_port='{ip_port}'")
            self.conn.commit()
            return 0
        except Exception as e:
            return -1

    def close(self):
        """
        关闭数据库
        :return:
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as ex:
            raise Exception("关闭数据库连接失败")
