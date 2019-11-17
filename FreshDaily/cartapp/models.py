from django.db import models

# 用户和商品：1对多
# 商品和用户：1对多
# 双向一对多就是多对多
# 从购物车页面可以看到：需要存着一个用户和商品以及购买数量的关系
class Cart(models.Model): # 第三张表
    user = models.ForeignKey('userapp.UserInfo', on_delete=models.CASCADE) # 跨app引入模型类可以用符号.
    good = models.ForeignKey('goodsapp.GoodsInfo', on_delete=models.CASCADE)
    # 增加一个数量字段
    count = models.IntegerField()