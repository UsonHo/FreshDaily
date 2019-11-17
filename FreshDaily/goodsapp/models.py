from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=10, verbose_name='商品类型')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')
    def __str__(self):
        return self.ttitle

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20, verbose_name='商品标题')
    gpic = models.ImageField(upload_to='goodsPic', verbose_name='商品图片')
    gprice = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='商品价格')
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')
    gunit = models.CharField(max_length=10, default='500g', verbose_name='单位')
    gclick = models.IntegerField(verbose_name='商品人气')
    gbrief = models.CharField(max_length=100, verbose_name='商品简介')
    gstock = models.IntegerField(verbose_name='商品库存') # 库存
    gcontent = HTMLField(verbose_name='详情内容')
    gtype = models.ForeignKey('TypeInfo', on_delete=models.CASCADE, verbose_name='商品类型')
