from django.contrib import admin

from goodsapp import models
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gstock', 'gcontent', 'gtype']

admin.site.register(models.TypeInfo, TypeInfoAdmin)
admin.site.register(models.GoodsInfo, GoodsInfoAdmin)
