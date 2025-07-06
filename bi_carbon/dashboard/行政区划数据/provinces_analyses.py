import pandas as pd

df = pd.read_excel('行政区划代码.xlsx',dtype='str')
df = df[df['行政区划代码'].notna()]
codes = df['行政区划代码']
province_codes = codes[codes.str.endswith('0000')]

provinces = df[df['行政区划代码'].isin(province_codes)]
# print(provinces)

import time
import requests

def get_location_by_name(name):
	while True:
		url = f'http://api.map.baidu.com/place/v2/search?query={name}&region={name}&output=json&ak=SMWRSDldnUUbz3k1zqOYMwChOZAGrttt'
		req = requests.get(url)
		result = req.json()
		print(result)
		if result['message'] =='ok':
			try:
				if 'location' in result['results'][0]:
					location = result['results'][0].get('location',[])
					return [location['lng'],location['lat']]
				else:
					return []
			except:
				return[]
		else:
			print('请求出错')

province_locations = {}
for province in provinces['单位名称']:
	province_locations[province] = get_location_by_name(province)
	time.sleep(0.2)
print(province_locations)