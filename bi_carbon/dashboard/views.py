from django.shortcuts import render
from django.http import JsonResponse
import json
import pytz
import uuid
from datetime import datetime
from django_pandas.io import read_frame
from dashboard.models import User,Comment,Order,Carbon
from django.core.paginator import Paginator
import pandas as pd
import numpy as np
from . import data_analysis
from django_q.tasks import async_task
from django.core.cache import cache



# Create your views here.

PAYMENT_PENDING = 'PE'
PAYMENT_SUCCESS = 'SU'
PAYMENT_CANCELLED = 'CA'
PAYMENT_OVERDUE = 'OV'
PAYMENT_REFUND = 'RE'
STATUS_TYPE_CHOICES = dict([
	(PAYMENT_PENDING, '未支付'),
	(PAYMENT_SUCCESS, '支付成功'),
	(PAYMENT_CANCELLED, '取消'),
	(PAYMENT_OVERDUE, '过期'),
	(PAYMENT_REFUND, '退款')
])

op_to_lookup = {
	'equal':'exact',
	'not_equal':'exact',
	'like':'contains',
	'not_like':'contains',
	'starts_with':'startswith',
	'ends_with':'endswith',
	'less':'lt',
	'less_or_equal':'let',
	'greater':'gt',
	'greater_or_equal':'gte',
	'between':'range',
	'not_between':'range',
	'select_equals':'exact',
	'select_not_equals':'exact',
	'select_any_in':'in',
	'select_not_any_in':'in',
}

data_analysis_function_map = {
	'provinces_carbon_map':data_analysis.get_provinces_carbon_map,
	'platform_pie':data_analysis.get_platform_pie,
	'product_line_income_bar':data_analysis.get_product_line_income_bar,
	'daily_income_line':data_analysis.get_daily_income_line,
	'total_income_text':data_analysis.get_total_income_text,
	'provinces_sales_map':data_analysis.get_provinces_sales_map,
}

def order_data_vis_api(request):
	data_type = request.GET.get('type','')
	data = {
		"status":0,
		"msg":"ok",
		"data":{}

	}

	sid = request.GET.get('sid','')
	if len(sid) ==0:
		return JsonResponse(data)
		
	cache_data = cache.get(sid)
	orders_df = pd.read_json(cache_data)
	# orders = SearchRecord.objects.get(id=sid).objs.all()
	# orders_df = read_frame(orders,coerce_float=True)
	data_analysis_function = data_analysis_function_map[data_type]
	data['data'] = data_analysis_function(orders_df)

	return JsonResponse(data)

def analyse_order_conditions(condithons):#amis条件转换成django能识别的内容
	final_query = None
	for child in condithons['children']:
		if 'children' in child:
			child_query = analyse_order_conditions(child)
		else:
			model,field = child['left']['field'].split('.')
			lookup = op_to_lookup[child['op']]
			right = child['right']
			if field.endswith('time'): 
				if isinstance(right,list):
					start_dt,end_dt =right
					dateArray = datetime.utcfromtimestamp(int(start_dt))
					start_dt = dateArray.strftime("%Y-%m-%dT%H:%M:%S%z")
					start_dt = start_dt+"+08:00"
					dateArray = datetime.utcfromtimestamp(int(end_dt))
					end_dt = dateArray.strftime("%Y-%m-%dT%H:%M:%S%z")
					end_dt = end_dt+"+08:00"
					start_dt = datetime.strptime(start_dt,'%Y-%m-%dT%H:%M:%S%z')
					end_dt = datetime.strptime(end_dt,'%Y-%m-%dT%H:%M:%S%z')
					right = (start_dt,end_dt)
				else:					
					dateArray = datetime.utcfromtimestamp(int(right))
					right = dateArray.strftime("%Y-%m-%dT%H:%M:%S%z")
					right = right+"+08:00"
					right = datetime.strptime(right,'%Y-%m-%dT%H:%M:%S%z')# right = datetime.fromtimestamp(int(right))

			if model == 'order':
				params = {f'{field}__{lookup}':right}
			else:
				params = {f'{model}__{field}__{lookup}':right}
			if 'not_' in child['op']:
				child_query = Order.objects.exclude(**params)
			else:
				child_query = Order.objects.filter(**params)
	if final_query is None:
		final_query = child_query
	elif condithons['conjunction'] == 'and':
		final_query = final_query & child_query
	else:
		final_query = final_query | child_query
	return final_query

def order_filter_api(request):
	data = json.loads(request.body.decode())#解码
	page = data.get('page',1)
	per_page = data.get('perPage',10)

	conditions = data.get('conditions',{})
	orders = analyse_order_conditions(conditions) if len(conditions) >0 else Order.objects.all()
	orders = orders.order_by('id')

	paginator = Paginator(orders,per_page)
	page_obj = paginator.get_page(page)
	items = list(page_obj.object_list.values())
	for item in items:
		item['carbon'] = Carbon.objects.get(id=item['carbon_id']).title
		item['create_time'] = item['create_time'].astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
		item['status'] = STATUS_TYPE_CHOICES[item['status']]
		if item['pay_time'] is not None:
			item['pay_time'] = item['pay_time'].astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
	data = {
		'status':0,
		'msg':"ok",
		"data":{
			"total":orders.count(),
			"items":items
		}
	}

	if len(conditions) > 0:
		# search_record = SearchRecord.objects.create(conditions=json.dumps(conditions))
		# search_record.objs.add(*orders)
		sid = str(uuid.uuid4())
		data['data']['sid'] = sid

		orders_df = read_frame(orders,coerce_float=True)
		orders_df["create_time"] = orders_df["create_time"].apply(lambda t:t.timestamp())
		print(orders_df["pay_time"])	
		for i in orders_df["pay_time"]:
			try:
				i.timestamp()
			except:
				i  = ''
		print(orders_df["pay_time"])
		# orders_df["pay_time"] = orders_df["pay_time"].apply(lambda t:t.timestamp())

		orders_json = orders_df.to_json()
		cache.set(sid,orders_json,600)
		

	return JsonResponse(data)

def order_send_email_api(request):
	sid = request.GET.get('sid')
	data = json.loads(request.body.decode())
	email = data.get('email')
	email_data = {
		'sid':sid,
		"email":email,
		'subject':'您的订单数据表格已生成',
	}

	async_task('dashboard.tasks.send_email',email_data)

	data = {
		'status':0,
		'msg':"邮件发生请求已经开始处理",
		"data":{
		}
	}

	return JsonResponse(data)


def charts_data(request):
	data = {
	  "status": 0,
	  "msg": "ok",
	  "data": {}
	}

	data_type = request.GET.get("type",'')

	data_analysis_function  = data_analysis_function_map[data_type]
	data['data'] = data_analysis_function()


	return JsonResponse(data)
	
def api_comment(request):
	data = json.loads(request.body.decode())
	per_page = data.get('perPage',10)
	page = data.get('page',1)
	rich_text = data.get('rich-text','')
	input_name = data.get('user_name','')
	rich_text = rich_text.split('\n')
	comment_detail = ""
	subtitle=' '
	for text in rich_text:
		if "</h1>" in text:
			title = text[3:-5]
		elif "</h2>" in text:
			subtitle = text[4:-4]
		else:
			comment_detail += text+'\n'

	subcomment = comment_detail[:comment_detail.find('\n')]

	print(rich_text)
	input_password = data.get('password','')
	if len(input_password)>0:
		data_base_name = User.objects.get(name=f'{input_name}')
		for i in list(User.objects.filter(name=f"{input_name}").values()):
			User_password = i["password"] 
		if User_password==input_password:
			comment = Comment(
				author = data_base_name,
				comment_title  = title,
				comment_subtitle = subtitle,
				comment = comment_detail,
				subcomment = subcomment,
				)
			comment.save()
	
	comments = Comment.objects.all()
	comments = comments.order_by('id')

	paginator = Paginator(comments,per_page)
	page_obj = paginator.get_page(page)
	items = list(page_obj.object_list.values())
	for item in items:
		item['author_id']=str(User.objects.get(id = item['author_id']))
		print(item['comment_time'])
	
	data = {
		"status":0,
		"msg":"ok",
		"data":{
			"total":comments.count(),
			"items":items
		}
	}
	return JsonResponse(data)

def comment_detail(request,comment_id):
	comment = Comment.objects.filter(id=comment_id).values()
	for comment in comment:
		comment['author_id'] = str(User.objects.get(id = comment['author_id']))
	print(comment)
	return render(request,'dashboard/post.html',{"comment":comment})

def index(request):
	pass
	return render(request,'dashboard/index.html')


def data_page(request):
	pass
	return render(request,'dashboard/data_page.html')

def about(request):
	pass
	return render(request,'dashboard/about.html')

def comment(request):
	pass
	return render(request,'dashboard/comment.html')

def carbon_trade(request):
	order_fields = [{'name':field.name,'label':field.verbose_name} for field in Order._meta.fields]
	return render(request,'dashboard/carbon_trade.html',{'order_fields':order_fields})





	


