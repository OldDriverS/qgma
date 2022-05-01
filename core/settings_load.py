from core.operation_txt import *
from core.text_mgt import *

try: bot_user_id = str(Text_Mgt.List_Read_Text('settings/basic/bot_user_id.txt','#')[0])
except: bot_user_id = ''
try: group_manage = Text_Mgt.List_Read_Text('settings/basic/group_manage.txt','#')[0:6]
except: group_manage = []
try: admin_user_id = Text_Mgt.List_Read_Text('settings/basic/admin_user_id.txt','#')[0:3]
except: admin_user_id = []
try: curfew_time = Text_Mgt.List_Read_Text('settings/basic/curfew_time.txt','#')[0:2]
except: curfew_time = []
try: task_cycle = int(Text_Mgt.List_Read_Text('settings/basic/task_cycle.txt','#')[0])
except: task_cycle = 4320
try: report_cycle = Text_Mgt.List_Read_Text('settings/basic/report_cycle.txt','#')[0:2]
except: report_cycle = []

try: server_send_port = int(Text_Mgt.List_Read_Text('settings/server/server_send_port.txt','#')[0])
except: server_send_port = 5700
try: server_rec_port = int(Text_Mgt.List_Read_Text('settings/server/server_rec_port.txt','#')[0])
except: server_rec_port = 5701
try: server_ip = str(Text_Mgt.List_Read_Text('settings/server/server_ip.txt','#')[0])
except: server_ip = '0.0.0.0'

try: del_msg_time = int(Text_Mgt.List_Read_Text('settings/member/del_msg_time.txt','#')[0])
except: del_msg_time = None
try: gag_num = int(Text_Mgt.List_Read_Text('settings/member/gag_num.txt','#')[0])
except: gag_num = None
try: fault_num = int(Text_Mgt.List_Read_Text('settings/member/fault_num.txt','#')[0])
except: fault_num = None
try: gag_time = Text_Mgt.List_Read_Text('settings/member/gag_time.txt','#')[0:64]
except: gag_time = [10]

try: ads_word = Text_Mgt.List_Read_Text('settings/word/ads_word.txt','#')[0:256]
except: ads_word = []
try: bad_word = Text_Mgt.List_Read_Text('settings/word/bad_word.txt','#')[0:256]
except: bad_word = []
try: ads_word_tips = Text_Mgt.List_Read_Text('settings/chat/ads_word_tips.txt','#')[0:64]
except: ads_word_tips = []
try: bad_word_tips = Text_Mgt.List_Read_Text('settings/chat/bad_word_tips.txt','#')[0:64]
except: bad_word_tips = []