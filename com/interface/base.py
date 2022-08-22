from com.other.log import login
from com.other.heade import get_user_agent
from com.pysqlit.py3 import IPsql


class BaseData:
    def __init__(self):
        self.sql = IPsql()
        self.log_write = login
        self.user_agent = get_user_agent()

