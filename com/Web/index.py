from flask import Flask

from com.detect.write_file import WriteFile
from com.ipS.get_nofree_ip_module import GetNoFreeIp
from com.other.conn import read_yaml
from com.other.log import rz
from com.other.order import Order

port = read_yaml()
app = Flask(__name__)
WF = WriteFile()
Order = Order()
GNF = GetNoFreeIp()
ip_pause_flags = False


@app.route("/")
def index():
    return "你好本程序运行正常运行"


@app.route('/log', methods=['GET'])
def cat_log():
    return rz()


# @app.route('/regetip', methods=['GET'])
# def re_get_ip():
#     Order.get_ip()
#     return "重新爬取ip任务提交成功"


@app.route('/pause', methods=['GET'])
def pause_ip():
    global ip_pause_flags
    ip_pause_flags = True
    return "已暂停分配IP"


@app.route('/continue', methods=['GET'])
def continue_ip():
    global ip_pause_flags
    ip_pause_flags = False
    return "恢复分配IP"


@app.route('/getall', methods=['GET'])
def get_all_ip():
    return Order.get_all_acting_ip()


@app.route('/api/mod/<_url>', methods=['GET'])
def revise_api(_url):
    Order.revise_api(_url)
    return "提交修改！"


# 接收get请求 /http
@app.route("/http", methods=["GET"])
def http():
    """
    代理的接口
    :return: 返回协议://ip:端口
    """
    global ip_pause_flags
    if ip_pause_flags:
        return 'http://127.0.0.1'
    result = GNF.get_nofree()
    if result == -1:
        result = WF.check_node()
    # 若检查不过，返回127.0.0.1
    return result if result != -1 else 'http://127.0.0.1'


def run_web():
    app.run(
        host='0.0.0.0',
        port=port['port'],
        debug=False
    )
