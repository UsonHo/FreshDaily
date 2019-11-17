from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from cartapp import views
app_name = 'cartapp'

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.cart, name='cart'),
    url(r'^add_(?P<gid>\d+)_(?P<cid>\d+)/$', views.addcart, name='addcart'),

    # 第一种方式
    url(r'^del_(?P<gid>\d+)_(?P<cid>\d+)/$', views.delcart, name='delcart'),
    # Ajax方式删除操作（这是第二种方式）
    url(r'^delete_(?P<ctid>\d+)/$', views.delete, name='delete'),

    # 已移步至orderapp模型设计中，停用
    url(r'^post_order/$', views.post_order, name='post_order'),
]