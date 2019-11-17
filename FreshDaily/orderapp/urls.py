from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from orderapp import views
app_name = 'orderinfo'

urlpatterns = [
    url(r'^$', views.order, name='order'),
]