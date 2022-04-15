from copyreg import clear_extension_cache


def Read_Txt(file):
    try: # UTF-8编码读取并去掉换行符，以列表形式输出
        with open(file, "r", encoding="utf-8") as txt_File:
            TEMP0 = txt_File.readlines()
        TEMP2 = [TEMP1.strip() for TEMP1 in TEMP0 if TEMP1.strip("\n") != ""]
        return TEMP2
    except: # GBK编码读取并去掉换行符，以列表形式输出
        try:
            with open(file, "r", encoding="gbk") as txt_File:
                TEMP0 = txt_File.readlines()
            TEMP2 = [TEMP1.strip()
                     for TEMP1 in TEMP0 if TEMP1.strip("\n") != ""]
            return TEMP2
        except:
            print("错误 - Error：\n程序运行时遇到了错误，以下是常见的原因：\n1.“" + file + "”文件不存在\n2.“" + file + "”使用了不支持的文件编码（仅支持GBK和UTF-8）\n\nThe program encountered errors while running,the following are common reasons:\n1.The \"" +
                  file + "\" file does not exist\n2.\"" + file + "\" uses unsupported file encoding (Only GBK and UTF-8 are supported).")
            quit()

def Write_Txt(file):
    pass

def Clear_Txt(file): # 删除TXT文件中第二行以后的内容
    try: # UTF-8编码读取首行并去掉换行符，之后重新写入首行
        with open(file, "r", encoding="utf-8") as txt_File:
            TEMP0 = txt_File.readline().strip('\n')
        with open(file, "w", encoding="utf-8") as txt_File:
            txt_File.write(str(TEMP0) + '\n')
    except: # GBK编码读取并去掉换行符，之后重新写入首行
        try:
            with open(file, "r", encoding="gbk") as txt_File:
                TEMP0 = txt_File.readline().strip('\n')
            with open(file, "w", encoding="gbk") as txt_File:
                txt_File.write(str(TEMP0) + '\n')
        except:
            print("错误 - Error：\n程序运行时遇到了错误，以下是常见的原因：\n1.“" + file + "”文件不存在\n2.“" + file + "”使用了不支持的文件编码（仅支持GBK和UTF-8）\n\nThe program encountered errors while running,the following are common reasons:\n1.The \"" +
                  file + "\" file does not exist\n2.\"" + file + "\" uses unsupported file encoding (Only GBK and UTF-8 are supported).")
            quit()