from flask import Flask

from com.detect.write_file import WriteFile
from com.other.conn import read_yaml
from com.other.log import rz

port = read_yaml()
app = Flask(__name__)
WF = WriteFile()


@app.route("/")
def index():
    return "你好本程序运行正常运行"


@app.route('/log', methods=['GET'])
def cat_log():
    return rz()


# 接收get请求 /http
@app.route("/http", methods=["GET"])
def js():
    """
    代理的接口
    :return: 返回协议://ip:端口
    """
    result = WF.check_node()
    # 若检查不过，返回127.0.0.1
    return result if result != -1 else 'http://127.0.0.1'


def run_web():
    app.run(
        host='0.0.0.0',
        port=port['port'],
        debug=False
    )
