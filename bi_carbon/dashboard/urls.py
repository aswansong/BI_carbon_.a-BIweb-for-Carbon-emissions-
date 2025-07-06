from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('about',views.about),
    path('data_page',views.data_page),
    path('comment',views.comment),
    path('api/global/charts_data',views.charts_data),
    path('api/comment',views.api_comment),
    path('carbon_trade',views.carbon_trade),
    path('api/order/filter',views.order_filter_api),
    path('api/order/data_vis',views.order_data_vis_api),
    path('api/order/send_email',views.order_send_email_api),
    path('comment/<int:comment_id>',views.comment_detail)
]