from flask import Flask

from com.detect.write_file import check_node
from com.other.conn import read_yaml

port = read_yaml()
app = Flask(__name__)


@app.route("/")
def index():
    return "你好本程序运行正常运行"


# 接收get请求 /js
@app.route("/js", methods=["GET"])
def js():
    """
    代理的接口
    :return: 返回协议://ip:端口
    """
    result = check_node()
    # 若检查不过，返回空代理
    return result if result != -1 else ' '


def run_web():
    app.run(
        host='0.0.0.0',
        port=port['port'],
        debug=False
    )
