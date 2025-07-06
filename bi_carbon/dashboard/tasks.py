import time
from tempfile import TemporaryDirectory
from datetime import datetime
import pandas as pd
import yagmail
from django.core.cache import cache


def task1(name):
	print('hello')
	time.sleep(3)
	print(name)

def send_email(data):
	print(data)
	with TemporaryDirectory() as tmp_folder:
		cache_data = cache.get(data['sid'])
		orders_df = pd.read_json(cache_data)
		dt = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
		file_path = f'{tmp_folder}/{dt}.csv'
		orders_df.to_csv(file_path, encoding='gbk')

		yag = yagmail.SMTP(user= '1025971724@qq.com',password='jjpfweisslvfbdbd',host='smtp.qq.com')
		content = ['订单数据表格请见附件。', file_path]
		yag.send(data['email'], data['subject'], content)

	return True
		
