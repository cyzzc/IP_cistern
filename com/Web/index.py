from flask import Flask, request, render_template

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


@app.route('/', methods=['GET', 'POST'])
def register():
    """停止恢复IP分配"""
    global ip_pause_flags
    mark = "你没有提交任何内容"
    if request.method == 'POST':
        tf = request.form.get('tf')
        url = request.form.get('url')
        if url:
            Order.revise_api(url)
            mark = "提交API成功"
        if tf == "start":
            ip_pause_flags = False
            return "恢复分配IP"
        elif tf == "stop":
            ip_pause_flags = True
            return "已暂停分配IP"
        else:
            return mark
    else:
        return render_template('ip.html')


@app.route('/log', methods=['GET'])
def cat_log():
    return rz()


# @app.route('/regetip', methods=['GET'])
# def re_get_ip():
#     Order.get_ip()
#     return "重新爬取ip任务提交成功"


@app.route('/getall', methods=['GET'])
def get_all_ip():
    all = Order.get_all_acting_ip()
    if len(all) > 0:
        return render_template('check.html', name=all)
    else:
        return "没有可用代理"


# @app.route('/api/mod/<_url>', methods=['GET'])
# def revise_api(_url):
#     Order.revise_api(_url)
#     return "提交修改！"


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
