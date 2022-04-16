def send_msg(msg):
    import requests # 需要安装
    try:res=requests.post(url='http://127.0.0.1:5700', data={"group_id":'1027033288','message':msg})
    except ConnectionError:print('error')
    print(str(res))