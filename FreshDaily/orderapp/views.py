from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from orderapp import models
from goodsapp.views import auth_login
from cartapp.models import Cart
from userapp.models import UserInfo

from django.db import transaction
from datetime import datetime
from decimal import Decimal

@auth_login
def order(request):
    if request.method == 'GET':
        uid = request.session.get('user_id')
        userobj = UserInfo.objects.get(pk=uid)
        addr_dic = userobj.uaddrs.values('pro').first()
        # print(addr_dic)
        cids = request.GET.getlist('cid')
        # print(cids)
        # orderobj_list = models.OrderInfo.objects.filter(user_id=uid)

        cartobj_list = []
        for cid in cids:
            cartobj_list.append(Cart.objects.filter(pk=int(cid)).first())
            # print(cid, cartobj_list)
        content = {'title': '提交订单页', 'page_name': 1, 'page_char': '提交订单',
                   'cartobj_list': cartobj_list, 'addr': addr_dic.get('pro')}

        return render(request, 'orderinfo/order.html', content)

    '''
    事务：一旦操作失败，则全部回退
    from django.db import transaction 
    1、创建订单对象
    2、判断商品库存
    3、创建详单对象
    4、修改商品库存
    5、删除购物车
    '''
    if request.method == 'POST':
        # 开始设置事务操作
        tran_id = transaction.savepoint()

        # 接收购物车编号
        cids = request.POST.get('cids')
        cid_list = cids.split(',')
        print("cid_list>>", cid_list)

        addr = request.POST.get('address')
        total = request.POST.get('total')
        print(addr, total)

        # 创建订单对象
        try:
            orderobj = models.OrderInfo()
            now_time = datetime.now()

            uid = request.session.get('user_id')
            orderobj.oid = '%s%d'%(now_time.strftime('%Y%m%d%H%M%S'), uid)
            orderobj.user_id = uid
            orderobj.odate = now_time
            orderobj.oaddress = addr
            orderobj.ototal = Decimal(total)

            orderobj.save()

            for cid in cid_list:
                # 创建详单对象
                oderdetailobj = models.OrderDetailInfo()

                cobj = Cart.objects.get(pk=int(cid))
                # 判断商品库存
                good = cobj.good
                if good.gstock >= cobj.count:
                    # 减少商品库存
                    good.gstock -= cobj.count
                    good.save()

                    oderdetailobj.goods_id = cobj.good_id
                    oderdetailobj.count = cobj.count
                    oderdetailobj.price = cobj.good.gprice
                    oderdetailobj.order_id = orderobj.oid

                    oderdetailobj.save()

                    # 删除购物车
                    cobj.delete()
                else:
                    transaction.savepoint_rollback(tran_id)
                    data = {'status': False}
                    return JsonResponse(data)

            orderobj.oIsPay = True
            orderobj.save()
            transaction.savepoint_commit(tran_id)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(tran_id)
            data = {'status': False}
            return JsonResponse(data)

        data = {'status': True}
        return JsonResponse(data)