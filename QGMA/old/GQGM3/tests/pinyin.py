'''
from xpinyin import Pinyin
test = Pinyin.get_pinyin('我的','')
print(str(test))
'''
#简单使用一下
from xpinyin.Pinyin import Pinyin
p = Pinyin() 
result = p.get_pinyin('小琳爱分享')  #此处结果：xiao-lin-ai-fen-xiang
result = p.get_pinyin('小琳爱分享','') #此处结果：xiaolinaifenxiang
result = Pinyin.get_pinyin('小琳爱分享',' ') #此处结果：xiao lin ai fen xiang
print(result) #结果：xiao-lin-ai-fen-xiang