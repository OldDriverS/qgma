import re

from regex import T
file = './start.txt'
rule = re.compile(r"[^a-zA-Z\u4e00-\u9fa5]")
with open(file, "r", encoding="utf-8") as txt_File:
    TEMP0 = txt_File.readlines()
    f=[]
    for z in TEMP0:
        f.append(rule.sub('',z))
    TEMP2 = [f.strip() for f in TEMP0 if f.strip("\n") != ""]
    TEMP2 = set(TEMP2)
with open('./over.txt', "w+",encoding='utf-8') as i:
    y=''
    for x in TEMP2:
        y +=(str(x) + '\n')
    i.write(y)

