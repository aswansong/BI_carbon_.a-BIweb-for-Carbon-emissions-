from django.contrib import admin
from .models import  User,Comment,Order,Carbon
# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Carbon)
