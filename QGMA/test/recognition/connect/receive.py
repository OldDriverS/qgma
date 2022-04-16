# 接收上报的事件，感谢"皮小孩ls"的文章：https://blog.csdn.net/qq_44809707/article/details/119959864
# 接收长消息：https://developer.aliyun.com/article/456224
# 稽术宅

import socket,json

server_ip = '0.0.0.0'
server_rec_port = 5701

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind((server_ip, server_rec_port))
ListenSocket.listen(100)
HttpResponseHeader = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i]=="{" and msg[-1]=="\n":
            return json.loads(msg[i:])
    return None
#需要循环执行，返回值为json格式
def rev_msg():# json or None
    Client, Address = ListenSocket.accept()
    # 长数据接收
    total_data = bytes()
    cycle_num = 0 # 循环计数，以防接收数据过长
    while True:
    # 将收到的数据拼接起来
        rev_data = Client.recv(1024)
        total_data += rev_data
        cycle_num += 1
        if len(rev_data) < 1024: # 如果数据接收完成
            break
        elif cycle_num >= 256:
            return None # 数据过长（大于256kb）的返回内容

    Request = total_data.decode(encoding='utf-8')
    rev_json = request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    #print(rev_json)
    return rev_json




if __name__ == '__main__':
    while 1:
        try:
            rev = rev_msg()
            if rev == None:
                continue
        except:
            continue
        print(str(rev)+'\n--------------------------')