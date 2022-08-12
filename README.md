# 新版本将在2022-08-12晚上发布，新版本将支持JS代理
# 青龙使用代理池来避免黑IP问题
## 此文档默认为最新文档，同步脚本更新此文档
## 需要下载 ip_broker.py 、kill.py 和 copy_ip、con.yml目录的文件，否则报错
#### 本脚本可能有一些其他问题存在，出现问题请反馈
## 运行脚本
安装所需库
```pip3
pip3 install -r requirements.txt
```
测试脚本是否正常
```shell
python3 ip_broker.py
```
先运行上面命令查看脚本是否有问题，没有问题运行下面命令进行，ip_broker.py只是检测脚本是否设置正确
运行脚本并添加守护进程

```shell
python3 kill.py
```

脚本自动添加守护进程，只需python3 kill.py即可，请勿再添加守护进程，使用python3 kill.py可以杀死原来全部ip_broker.py的所有守护进程，而后创建新的
运行后请查看ql_acting.log日志是否有异常信息

## [青龙代理视频演示](https://www.youtube.com/playlist?list=PLH5cFwS6-yF-yDy-eGA3nVVa-2Nl43ZKk)

## 文件配置conn.yml

```text
第3行青龙配置文件路径
第6行代理添加行数 (不能最后一行)
第9行日志输出路径
第12行虚拟数据库存储路径
第15行代理筛选
第18行取消添加代理的时间，建议提前几秒，不支持日期，精确到秒
```

## 下面是在青龙里面运行py文件检测到的IP

<img src="./img/demo.jpg" alt="">
<br>

## 青龙面板添加依赖

依赖管理-->Python3-->新建依赖

```text
requests
pysocks
```

<img src="./img/re.jpg" alt="">

### 使用报错

如果运行提示图片 import ****** 报错 请安装 pip install ******，或者百度搜索 import ******,
pyyaml = yaml 是用来读取yaml文件的库
根据需代码提示缺少依赖添加

<img src="./img/cw.jpg" alt="错误提示缺少依赖库">

### 查看是否添加成功

在青龙脚本管理-->新建脚本-->ip.py
把下内容进去，然后调试，脚本选择python,然后运行，如果显示代理IP表示添加成功

```python
import requests
aas = requests.get("https://ip.tool.lu/")
print("检测到的IP", aas.text)
```

<details>
  <summary>不可用的代理池</summary>
  <pre><code> 
http://ip.yqie.com/ipproxy.htm 确认不可用
http://www.xsdaili.cn/ 没看到更新，放弃
http://www.taiyanghttp.com/free 放弃没有可用的
https://www.toolbaba.cn/ip 不可用
https://www.atomintersoft.com/high_anonymity_elite_proxy_list 不可用
https://ab57.ru/downloads/proxyold.txt 不可用
http://www.proxylists.net/http_highanon.txt 不可用
https://www.my-proxy.com/free-proxy-list-2.html 不可用
http://www.cybersyndrome.net/pla6.html 不可用
https://www.cnproxy.com/proxy1.html 不可用
https://www.89ip.cn/index_1.html 不可用
http://www.kxdaili.com/dailiip/2/1.html 不可用
http://emailtry.com/index/1 不可用
https://pzzqz.com/ 不可用
http://nntime.com/ 不可用
https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1 不可用
https://openproxy.space/ 不可用
https://www.tyhttp.com/free/ 不可用
https://proxy11.com/ 不可用
  </code></pre>
</details>

<details>
  <summary>检测可用代理池</summary>
  <pre><code> 
http://proxylist.fatezero.org/ = http://proxylist.fatezero.org/proxy.list 可用率高
https://proxy.mimvp.com/freesecret 抓起来麻烦，端口是图片
https://freeproxylists.net/zh/ 1/10
http://www.kxdaili.com/dailiip.html 1/5
http://www.kxdaili.com/dailiip/2/1.html 1/10
http://pubproxy.com/api/proxy?limit=20&format=txt&type=http 不可用，偶尔可用
https://www.cool-proxy.net/ 九个出一个
https://proxy-list.org/english/index.php bs4加密，可能有反爬，国内不能直接访问，待测试可用时长
https://regex101.com/
https://ip.jiangxianli.com/ 13个出两个
https://www.freeproxylists.net/zh/ 1/20
https://www.proxy-list.download/HTTP 26出一个
http://www.kxdaili.com/dailiip/2/1.html 11个出一个
http://www.kxdaili.com/dailiip.html 9个出三个
http://www.cybersyndrome.net/pla6.html 1/20可用
http://www.cybersyndrome.net/pla6.html 1/10
https://spys.one/en/anonymous-proxy-list/ 一个可用
https://spys.one/en/https-ssl-proxy/ 两个
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt 1/1000
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt 可用率高
https://github.com/mertguvencli/http-proxy-list
https://github.com/monosans/proxy-scraper-checker
https://ip.ihuan.me/ 一个可用
https://hidemy.name/en/proxy-list/ 一个可用
https://www.us-proxy.org/ 5个
https://proxy.seofangfa.com/ 可以使用就一个检测成功的
  </code></pre>
</details>

<details>
  <summary>版本更新</summary>
  <pre><code> 
1.0版本
    > 修复运行多个线程守护而对配置文件照成合并乱码删除的BUG
1.1版本
    > 添加日志输出，输出位置为当前目录下的ql_acting.log
    > ql_acting.log > 10M 会清空日志
1.2版本
    > 换肉不换皮，基本能封闭的都分离的
    > 添加了sqlite3数据库，支持节点筛选
    > 添加国外代理
    > 优化代理检测速度，由原来单线程变成同时检测多个代理，极大减少了未来多节点的检测时间
    > 第一次运行会提示异常，第二次就没有问题了
1.2.1版本
    > 修复了sqlite3数据库获取上次数据问题，无法获取本次代理问题
    > 增加了代理检测，在添加到配置文件的时候又进行了一次检测，但是会导致脚本运行时间延长
1.2.2版本
    > 添加定时任务取消代理
1.2.3版本
    > 添加支持多个容器代理
未来版本
    > 逐渐向代理池方向发展
  </code></pre>
</details>

<details>
  <summary>问题</summary>
  <pre><code> 
代理添加上不能用
    > 青龙2.10版本支持代理版本未知，2.11支持，2.12支持
    > 代理池里IP只能保证添加的时候是可用的，但是添加后能用多久就不知道了，一般2-3分钟
代理池问题
    > 不确定抓取代理池多了是否会被封IP
    > 代理池抓取的IP安全性方面无法保证，请自行选择是否使用
    > 如果因为抓取过多，而被网址封IP，可反馈，有解决方案，但是怕被某些人攻击服务器，只能当备用方案
其他问题
    > 所有反馈都会尽量解决，但是因个人技术问题，不能保证解决所有问题
    > 以后反馈问题会在晚上十点左右回复，白天有时回复，但是不保证
    > 此脚本可能存在其他问题，请自行测试，并且反馈问题
    > 本人只能保证本人仓库的代码的没有任何偷取信息行为，如果有信息泄露，一切与本人无关
    > 此脚本仅限用于学习交流，代码在使用过程中，出现任何不法行为，本人将不承担任何责任
  </code></pre>
</details>
