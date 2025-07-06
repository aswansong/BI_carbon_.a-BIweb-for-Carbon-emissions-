请注意——您的系统中应该有以下的python第三方库：(python-3.8)

Package	Version
datetime	4.4
django	4.0.2
django_pandas	0.6.6
django-q	1.3.9
Faker	13.3.1
numpy	1.19.3
pandas	1.4.1
pytz	2021.3
uuid	1.30
yagmail	0.15.277

打开bi_carbon文件夹，找到有manage.py的文件夹目录，在当前的文件夹目录运行cmd命令行，在命令行中输入python manage.py runserver 
然后在本地浏览器中输入http://127.0.0.1:8000/，若页面成功打开，则运行成功。
由于异步任务系统的存在，故在页面达开成功的基础上，若想使用Django-q异步任务系统，
则需要另外开一个cmd命令行，运行django-q异步任务系统，其指令为：python manage.py qcluster。
