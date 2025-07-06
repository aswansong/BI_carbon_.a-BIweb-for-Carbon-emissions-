import pandas as pd
province_coordinates={'Beijing': [116.413387, 39.910924], 'Tianjin': [117.208091, 39.091103], 'Hebei': [114.536594, 38.0432], 'Shanxi': [112.569376, 37.879831], 'InnerMongolia': [111.772606, 40.823156], 'Liaoning': [123.435594, 41.841466], 'Jilin': [125.332582, 43.901713], 'Heilongjiang': [126.669656, 45.74793], 'Shanghai': [121.48054, 31.235929], 'Jiangsu': [118.769553, 32.066777], 'Zhejiang': [120.159537, 30.271549], 'Anhui': [117.330539, 31.734294], 'Fujiang': [119.302446, 26.10634], 'Jiangxi': [115.915421, 28.68169], 'Shandong': [117.027442, 36.674857], 'Heinan': [113.75938, 34.771713], 'Hubei': [114.348443, 30.5516], 'Hunan': [112.989604, 28.118269], 'Guangdong': [113.272426, 23.137949], 'Guangxi': [108.334522, 22.821268], 'Hainan': [110.355538, 20.025802], 'Chongqing': [106.558437, 29.568996], 'Sichuan': [104.073463, 30.577544], 'Guizhou': [106.714473, 26.604029], 'Yunnan': [102.71642, 25.051562], 'Xizang': [91.124344, 29.652894], 'Shaanxi': [108.960389, 34.275807], 'Gansu': [103.832475, 36.065466], 'Qinghai': [101.786458, 36.627158], 'Ningxia': [106.265607, 38.476878], 'Xinjiang': [87.633475, 43.799236], 'Tailand': [], 'Xianggang': [114.181517, 22.28293], 'Aomen': [113.551589, 22.19316]}
province_coordinates_chinese={'北京市': [116.413387, 39.910924], '天津市': [117.208091, 39.091103], '河北省': [114.536594, 38.0432], '山西省': [112.569376, 37.879831], '内蒙古自治区': [111.772606, 40.823156], '辽宁省': [123.435594, 41.841466], '吉林省': [125.332582, 43.901713], '黑龙江省': [126.669656, 45.74793], '上海市': [121.48054, 31.235929], '江苏省': [118.769553, 32.066777], '浙江省': [120.159537, 30.271549], '安徽省': [117.330539, 31.734294], '福建省': [119.302446, 26.10634], '江西省': [115.915421, 28.68169], '山东省': [117.027442, 36.674857], '河南省': [113.75938, 34.771713], '湖北省': [114.348443, 30.5516], '湖南省': [112.989604, 28.118269], '广东省': [113.272426, 23.137949], '广西壮族自治区': [108.334522, 22.821268], '海南省': [110.355538, 20.025802], '重庆市': [106.558437, 29.568996], '四川省': [104.073463, 30.577544], '贵州省': [106.714473, 26.604029], '云南省': [102.71642, 25.051562], '西藏自治区': [91.124344, 29.652894], '陕西省': [108.960389, 34.275807], '甘肃省': [103.832475, 36.065466], '青海省': [101.786458, 36.627158], '宁夏回族自治区': [106.265607, 38.476878], '新疆维吾尔自治区': [87.633475, 43.799236], '台湾省': [], '香港特别行政区': [114.181517, 22.28293], '澳门特别行政区': [113.551589, 22.19316]}


def get_provinces_carbon_map():
	provinces_carbon = [{'name':'Shaanxi','value':[108.960389, 34.275807,'296.27254']},{'name': 'Shanghai', 'value': [121.48054, 31.235929, '192.912182']}, {'name': 'Yunnan', 'value': [102.71642, 25.051562, '185.95592']}, {'name': 'InnerMongolia', 'value': [111.772606, 40.823156, '794.279375']}, {'name': 'Beijing', 'value': [116.413387, 39.910924, '88.155437']}, {'name': 'Jilin', 'value': [125.332582, 43.901713, '203.661561']}, {'name': 'Sichuan', 'value': [104.073463, 30.577544, '315.163355']}, {'name': 'Tianjin', 'value': [117.208091, 39.091103, '158.466482']}, {'name': 'Ningxia', 'value': [106.265607, 38.476878, '212.413784']}, {'name': 'Anhui', 'value': [117.330539, 31.734294, '408.064341']}, {'name': 'Shandong', 'value': [117.027442, 36.674857, '937.116922']}, {'name': 'Shanxi', 'value': [112.569376, 37.879831, '566.484251']}, {'name': 'Guangdong', 'value': [113.272426, 23.137949, '585.810531']}, {'name': 'Guangxi', 'value': [108.334522, 22.821268, '246.716709']}, {'name': 'Xinjiang', 'value': [87.633475, 43.799236, '455.274574']}, {'name': 'Jiangsu', 'value': [118.769553, 32.066777, '804.594214']}, {'name': 'Jiangxi', 'value': [115.915421, 28.68169, '242.308256']}, {'name': 'Hebei', 'value': [114.536594, 38.0432, '914.209118']}, {'name': 'Zhejiang', 'value': [120.159537, 30.271549, '381.407216']}, {'name': 'Hainan', 'value': [110.355538, 20.025802, '43.067084']}, {'name': 'Hubei', 'value': [114.348443, 30.5516, '354.752471']}, {'name': 'Hunan', 'value': [112.989604, 28.118269, '310.641666']}, {'name': 'Gansu', 'value': [103.832475, 36.065466, '164.488403']}, {'name': 'Guizhou', 'value': [106.714473, 26.604029, '261.129235']}, {'name': 'Liaoning', 'value': [123.435594, 41.841466, '533.388436']}, {'name': 'Chongqing', 'value': [106.558437, 29.568996, '156.254673']}, {'name': 'Qinghai', 'value': [101.786458, 36.627158, '51.752403']}, {'name': 'Heilongjiang', 'value': [126.669656, 45.74793, '278.211338']}]
	min_value = 51.752403
	max_value = 937.116922
	return {"provinces_carbon":provinces_carbon,'min_value':min_value,"max_value":max_value}


def get_platform_pie(df):
	platform_counts = df['platform'].value_counts()
	platform_data = [{"name":name,"value":value} for name,value in platform_counts.items()]
	return {'platform_data':platform_data}


def get_product_line_income_bar(df):
	product_line_incomes = df[['product_line','price']].groupby('product_line').sum()
	product_line_incomes = product_line_incomes.sort_values(by = 'price',ascending=False)
	data = {
		'x_data':product_line_incomes.index.to_list(),
		'y_data':product_line_incomes['price'].to_list()
	}
	return data

def get_daily_income_line(df):
	orders_df = df[df['pay_time'].notna()]
	orders_df['pay_time'] = orders_df['pay_time'].dt.tz_localize('Asia/Shanghai')
	orders_df['pay_time'] = orders_df['pay_time'].dt.date
	start_data,end_data = orders_df['pay_time'].min(),orders_df['pay_time'].max()
	dates_index = pd.date_range(start_data,end_data)
	daily_income = pd.Series(index=dates_index,dtype='float64').fillna(0.0)
	groupby_pay_time_df = orders_df[['pay_time','price']].groupby('pay_time').sum()
	daily_income += groupby_pay_time_df['price']
	daily_income = daily_income.fillna(0.0)
	x_data = [dt.strftime("%Y-%m-%d") for dt in daily_income.index]
	y_data = daily_income.values.tolist()
	return {
		"x_data":x_data,
		"y_data":y_data
	}


def get_total_income_text(df):
	total_income = df['price'].sum()
	return {'total_income':str(total_income)}

def get_provinces_sales_map(df):
	def get_province_name(row):
		for province in provinces:
			if row.startswith(province):
				return province

	provinces =province_coordinates_chinese.keys()
	provinces_data = df['user_address'].apply(get_province_name)
	provinces_value_counts = provinces_data.value_counts()
	provinces_sales = []
	min_value = int(provinces_value_counts.min())
	max_value = int(provinces_value_counts.max())
	for index,value in provinces_value_counts.items():
		coordinates = province_coordinates_chinese[index]
		provinces_sales.append({'name':index,'value':coordinates+[value]})


	return {'provinces_sales':provinces_sales,'min_value':min_value,'max_value':max_value}


