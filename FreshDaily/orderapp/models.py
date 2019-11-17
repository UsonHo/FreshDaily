from django.db import models

class OrderInfo(models.Model):
    # 订单id
    oid = models.AutoField(max_length=20, primary_key=True)
    # 用户信息
    user = models.ForeignKey('userapp.UserInfo', on_delete=models.CASCADE)
    # 是否支付
    oIsPay = models.BooleanField(default=False)
    # 收货地址
    oaddress = models.CharField(max_length=100)
    # 下单时间
    odate = models.DateField(auto_now=True)
    # 支付总金额支持：最大6位，包括小数2位
    ototal = models.DecimalField(max_digits=6, decimal_places=2)

class OrderDetailInfo(models.Model):
    # 结算商品详细信息
    goods = models.ForeignKey('goodsapp.GoodsInfo', on_delete=models.CASCADE)
    # 结算商品单价
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 结算商品数量
    count = models.IntegerField()
    # 其他订单信息
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE)