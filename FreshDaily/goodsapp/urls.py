from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from goodsapp import views
app_name = 'goodsapp'

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^list(?P<tid>\d+)_(?P<pid>\d+)_(?P<oid>\d+)/$', views.list, name='list'),
    url(r'^detail_(?P<gid>\d+)/$', views.detail, name='detail'),

    # 搜索
    url(r'^search/',  views.FacetedSearchView(), name='search_view'),
]