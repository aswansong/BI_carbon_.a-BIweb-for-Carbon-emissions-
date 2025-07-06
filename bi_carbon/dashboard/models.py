from django.db import models

# Create your models here.

class Comment(models.Model):
	COMMENT_SUCCESS = 'SU'
	COMMENT_CANCELLED = 'CA'
	COMMENT_VIOLATION = 'VI'
	STATUS_TYPE_CHICES  =[
		(COMMENT_SUCCESS,'评论成功'),
		(COMMENT_CANCELLED,'评论取消'),
		(COMMENT_VIOLATION,'评论违规'),

	]

	cid = models.CharField('评论ID',max_length = 200,editable = False)
	author = models.ForeignKey('User',verbose_name="作者", on_delete=models.SET_NULL, blank=True, null=True)
	status = models.CharField('评论状态',max_length=2,choices=STATUS_TYPE_CHICES,default=COMMENT_SUCCESS)
	comment_title = models.CharField('评论标题',max_length=120)
	comment_subtitle = models.CharField('评论副标题',max_length=240,blank=True,null=True)
	subcomment = models.CharField('评论简介',max_length=100,default="暂无")
	comment = models.TextField('评论内容',max_length=5000,)
	comment_time = models.DateTimeField('评论时间',auto_now_add=True)

	def __str__(self):
		return self.comment_title

	class Meta:
		ordering = ['cid']
		verbose_name = 'Comment'



class User(models.Model):
	'''用户表'''

	name = models.CharField(max_length=128,unique=True)
	password = models.CharField(max_length=256)
	email = models.EmailField(unique=True)
	c_time = models.DateTimeField(auto_now_add=True)
 
	def __str__(self):
		return self.name
 
	class Meta:
		ordering = ['c_time']
		verbose_name = '用户'
		verbose_name_plural = '用户'


#碳排放交易平台
class Order(models.Model):
	oid = models.CharField("订单ID", max_length=20, editable=False)
	product_line = models.CharField("产品线", max_length=20)
	carbon = models.ForeignKey("Carbon", verbose_name="碳排放权", on_delete=models.SET_NULL, blank=True, null=True)
	create_time = models.DateTimeField("下单时间")
	user_id = models.CharField("用户ID", max_length=40)
	user_mobile = models.CharField("手机号", max_length=20)
	user_address = models.CharField("地址", max_length=200, blank=True, null=True)
	abtest = models.IntegerField("ABTest", blank=True, null=True)
	pay_time = models.DateTimeField("支付时间", blank=True, null=True)
	pay_channel = models.CharField("支付方式", max_length=20, blank=True, null=True)
	PAYMENT_PENDING = 'PE'
	PAYMENT_SUCCESS = 'SU'
	PAYMENT_CANCELLED = 'CA'
	PAYMENT_OVERDUE = 'OV'
	PAYMENT_REFUND = 'RE'
	STATUS_TYPE_CHOICES = [
		(PAYMENT_PENDING, '未支付'),
		(PAYMENT_SUCCESS, '支付成功'),
		(PAYMENT_CANCELLED, '取消'),
		(PAYMENT_OVERDUE, '过期'),
		(PAYMENT_REFUND, '退款')
	]
	status = models.CharField("订单状态", max_length=2, choices=STATUS_TYPE_CHOICES, default=PAYMENT_PENDING)
	transaction_serial_number = models.CharField("交易流水号", max_length=40, editable=False, blank=True, null=True)
	price = models.DecimalField("金额", max_digits=10, decimal_places=2)
	fee_price = models.DecimalField("手续费", max_digits=10, decimal_places=2, blank=True, null=True)
	refund_price = models.DecimalField("退款金额", max_digits=10, decimal_places=2, blank=True, null=True)
	out_vendor = models.CharField("渠道", max_length=100, blank=True, null=True)
	platform = models.CharField("下单来源", max_length=50, blank=True, null=True)

	def __str__(self):
		return self.oid

	class Meta:
		verbose_name = "order"


class Carbon(models.Model):
	cid = models.IntegerField("碳排放权交易ID")
	title = models.CharField("类型", max_length=30)
	price = models.DecimalField("交易额", max_digits=10, decimal_places=2)
	CDM, voluntary = 'C', 'V'
	CARBON_TYPE_CHOICES = [
		(CDM, '清洁发展机制'),
		(voluntary, '自愿减排')
	]
	carbon_type = models.CharField("付费类型", max_length=1, choices=CARBON_TYPE_CHOICES, default=CDM)

	def __str__(self):
		return str(self.title)

	class Meta:
		verbose_name = "Carbon"

class SearchRecord(models.Model):
	conditions = models.TextField("查询条件",blank=True,null = True)
	objs = models.ManyToManyField("order",blank=True)


	class Meta:
		verbose_name = '搜索记录'
