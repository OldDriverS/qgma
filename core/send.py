import requests # 需要安装
try:res=requests.post(url='http://0.0.0.0:5702', data={"user_id":'2993642371','message':'测试3'})
except:print('不允许')
print(str(res))