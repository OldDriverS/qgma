from urllib import parse
from http.cookiejar import CookieJar
import logging
import json
import ipaddress
import time
from bottle import Bottle, request
import re
from threading import Thread
from urllib.request import (Request, OpenerDirector, ProxyHandler, UnknownHandler,
                            HTTPHandler, HTTPDefaultErrorHandler,
                            HTTPRedirectHandler, FTPHandler,
                            FileHandler, HTTPErrorProcessor,
                            DataHandler, HTTPCookieProcessor)


class CQHTTPOpener(OpenerDirector):
    """CQHTTP访问器"""
    default_handlers = [ProxyHandler, UnknownHandler, HTTPHandler,
                        HTTPDefaultErrorHandler, HTTPRedirectHandler,
                        FTPHandler, FileHandler, HTTPErrorProcessor,
                        DataHandler]
    default_headers = [
        ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"),
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"), ]

    def __init__(self, host: str, port: int = 7500) -> None:
        """初始化访问器"""
        super().__init__()
        self.host, self.port = ipaddress.ip_address(host), port
        self.__cookie = CookieJar()
        for cls in self.default_handlers:
            self.add_handler(cls())
        self.add_handler(HTTPCookieProcessor(self.__cookie))
        self.addheaders += self.default_headers

    def post(self, rpc_method: str, **kw):
        """cqhttp api访问功能封装

            post(method, args ...)
            例如
                xxx.post("send_private_msg") 发送私聊信息，参数与cqhttp wiki中列出一致
                xx.post("send_msg", user_id=xxxx, message="xxxx")
        """
        kw = parse.urlencode(kw)
        kw = kw.encode("utf-8") if kw else None
        url = parse.urljoin(
            f"http://{self.host}:{self.port}", f"{rpc_method}")
        req = Request(url=url, data=kw, method="POST")
        rpc_response = super().open(req)
        return json.loads(rpc_response.read())

    def open(self, *args, **kw):
        return self.post(*args, **kw)


class EventNode:
    """事件节点

        事件节点作为一个可悲调用的对象，调用它等同于调用了对应的事件处理函数
        它可以：
          - 添加子事件，匹配更详细的第一个事件优先被执行
          - 搜索匹配子事件
          - 注册回调函数
    """

    def __init__(self, callback=None, **kw):
        self._match_dict = kw  # 匹配的字典
        self._sub_node = []  # 子节点
        self._callback = callback  # 回调
        self.mask = False  # 不屏蔽事件

    def __str__(self):
        return f'<{self.__class__.__name__} {self._match_dict} |>'

    def __repr__(self):
        return self.__str__()

    def __call__(self, kw):
        """节点可以被调用"""
        if not self._callback:
            return None
        if not self.mask:
            # 屏蔽后不可触发
            return self._callback(self, kw)

    def call(self, kw):
        """寻找一个匹配度较高的子节点并执行"""
        node = self.match(kw)
        if callable(node):
            node(kw)

    def set_callback(self, callback):
        if callable(callable):
            self._callback = callback
            return True
        return False

    def match(self, kw):
        """从子树中返回一个匹配的节点"""
        retnode = None
        is_match = True  # 默认选中
        # 查找公共元素
        match_keys = set(self._match_dict.keys())
        result = match_keys & set(kw.keys())
        if result != match_keys:  # 键不匹配
            return None
        for k, v in self._match_dict.items():
            # 判断v类型
            such_match_result = False  # 当前匹配结果
            if isinstance(v, re.Pattern):  # 正则匹配模式
                such_match_result = bool(v.search(kw[k]))
            elif callable(v):  # 函数匹配模式
                such_match_result = bool(v(kw[k]))
            else:  # 值匹配模式
                such_match_result = v == v.__class__(kw[k])
            is_match = is_match and such_match_result
        if not is_match:
            return None
        retnode = self  # 键值匹配选择自己
        # 递归进一步查找子节点，更详细的事件优先匹配
        for sub in self._sub_node:
            node = sub.match(kw)
            if node:
                retnode = node  # 覆盖低优先级的父节点
                break
        return retnode

    def childs(self):
        """返回子节点"""
        return self._sub_node

    def register(self, *args, **kw):
        """注册子事件

            - 注册一个函数会自动生成一个节点
            - 可以同时注册多个节点
            xxx.register(node1，node2,node3)
            def callback(**kw): pass
            xxx.register(a=100,b=200)(callback)
        """
        register_counter = 0
        for val in args:
            if isinstance(val, self.__class__):
                self._sub_node.append(val)
                register_counter += 1
        if register_counter:  # 不为0说明已经登记了N个事件
            return None

        # 如果是通过字符串注册，返回一个闭包接收回调函数
        # register_manager = xx.register(user_id=xxx)
        # register_manager(handler)

        def inner(callback):
            """接收回调函数"""
            if not callable(callback):
                raise Exception("参数必须是一个函数")
            sub_node = self.__class__(callback=callback, **kw)
            self._sub_node.append(sub_node)
            return callback
        return inner


class EventManager():
    """事件管理器
    """
    # 默认的日志格式
    log_default_format = '[%(levelname)s][%(name)s] %(message)s'
    # 预定义的匹配字典：基础事件大类
    post_type_message = {"post_type": "message"}  # 聊天事件
    post_type_request = {"post_type": "request"}  # 加群事件
    post_type_notice = {"post_type": "notice"}  # 提醒事件
    post_type_heartbeat = {"post_type": "meta_event"}  # 上报心跳
    # 常用事件
    private_message = {**post_type_message, "message_type": "private"}  # 私聊事件
    group_message = {**post_type_message, "message_type": "group"}  # 群聊事件
    group_request = {**post_type_request,
                     "request_type": "group", "sub_type": "add"}  # 加群事件
    group_leave = {**post_type_notice, "notice_type": "group_decrease"}  # 退群事件

    def __init__(self, cqhttp_host: str = "192.168.10.5", cqhttp_port: int = 80,
                 host="0.0.0.0", port: int = 8080, logger=None,
                 log_level: str = "INFO", log_format=None) -> None:
        """
            cqhttp_host,cqhttp_port : cqhttp 服务的IP与端口
            host, port: 用于监听cqhttp 上报事件的IP与端口
            logger : python 日志管理器, 可选，默认控制台输出
            log_level : 日志级别，默认 INFO
        """
        self.cqhttp = CQHTTPOpener(
            cqhttp_host, cqhttp_port)  # cqhttp访问器，调用cqhttp的api
        self._root_node = EventNode()  # 事件的根节点，默认匹配所有事件
        self._webfw = Bottle()  # web服务，用于接收cqhttp上报的事件
        self.host = host  # Bottle监听host
        self.port = port  # Bottle监听端口
        self.quiet = True  # 默认不打印Bottle日志
        if not logger:  # 设置logger
            logger = logging.getLogger(self.__class__.__name__)
            log_level = getattr(logging, log_level.upper()) if log_level.upper(
            ) in logging._nameToLevel.keys() else logging.INFO
            logger.setLevel(log_level)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                log_format if log_format else self.log_default_format))
            logger.addHandler(console_handler)
        self.logger = logger

        # 注册接收函数
        @self._webfw.route("/", ["POST", "GET"])
        def inner():
            try:
                self._root_node.call(request.json)
            except Exception as e:
                self.logger.error(f'事件触发致命错误：{repr(e)}')

    def setLogLevel(self, level):
        """更改日志的等级
            可选的值为 INFO ERROR WARNING WARN ..
            与logging一致
        """
        if isinstance(level, str):
            level = level.upper()
            if level not in logging._nameToLevel.keys():
                return False
            level = getattr(logging, level)
        elif not isinstance(level, int):
            return False
        self.logger.setLevel(level)

    def register(self, **kw):
        """注册事件"""
        return self._root_node.register(**kw)

    def run(self, **kw):
        for k in ["host", "port", "quiet"]:
            if not kw.get(k):
                kw[k] = getattr(self, k)
        self._webfw.run(**kw)


def substr(*args):
    """如果关键字列表key存在message中返回True"""
    def inner(message):
        for key in args:
            if key in message:
                return True
        return False
    return inner


def loadfile(filename: str):
    """读取文件中的关键字，一行一个"""
    with open(filename, "r", encoding="utf-8") as fd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            yield line

############
# 事件响应测试
############


"""
注册事件流程

1. 定义一个事件管理器 

root = EventManager(cqhttp_host="192.168.10.5",port=8080)

它可以做的事：
    - 接收cqhtp 发送过来的事件
    - 调用cqhttp(192.168.10.5:8080) 的接口
    - 注册匹配事件的处理函数 handler，当事件上报时自动触发
    - 匹配处理函数感兴趣的日志，支持的匹配模式：正则匹配，字符串完整匹配，自定义函数灵活匹配
    - 允许多条件匹配，多个条件同时成立才算匹配成功

2. 设定一个感兴趣的事件，例如接收信息中匹配到 `玛卡巴卡`，那么它的匹配参数是：
    post_type="message",message=re.compile("玛卡巴卡")
    
register_manager = root.register(post_type="message", message_type="private", message=re.compile("玛卡巴卡"))
也可以用预定义的事件字典
register_manager = root.register(**EventManager.private_message, message=re.compile("玛卡巴卡"))

    register 将返回一个函数，调用该函数可完成注册

3.编写一个针对该事件的处理函数handler，例如收到 `玛卡巴卡` 后，给对方也回复 `玛卡巴卡`

handler的原型为

def handler(event, kw): pass
event 是被触发的事件节点
kw 是一个字典，它是cqhttp返回的完整内容

这里将handler

def handler(event, **kw):
    root.logger.info(f"私聊：{kw['sender']['nickname']} 和你说了 {kw['message']}")
    root.cqhttp.post("send_private_msg",**{
        "user_id":kw["user_id"],
        "message":"暗号正确，玛卡巴卡~",
    })

4.将handler函数作为参数传递给register返回的函数register_manager即可完成事件注册
    register_manager(handler)

推荐使用装饰器的写法
@xxx.register(事件匹配列表..)
def handler(event,kw):
    pass

"""

