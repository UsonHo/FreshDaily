from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from userapp import views
app_name = 'userapp'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # url(r'^$', views.index),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_exist', views.register_exist, name='register_exist'),

    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^login_check2/$', views.login_check2, name='login_check2'),
    url(r'^login/$', views.login, name='login'),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^uinfo/$', views.uinfo, name='uinfo'),
    url(r'^uinfo_order/', views.uinfo_order, name='uinfo_order'),
    url(r'^uinfo_site/$', views.uinfo_site, name='uinfo_site'),
]