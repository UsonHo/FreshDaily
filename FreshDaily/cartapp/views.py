from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse

from cartapp import models
from userapp.models import UserInfo

from userapp.views import auth_login
from django.db.models import Count

@auth_login
def cart(request):
    uid = request.session.get('user_id')
    # 一个用户uid对应着多个商品数据gid，所以获取到的是一个第三张表cart的对象列表
    cartobj_list = models.Cart.objects.filter(user_id=uid)
    content = {'title': '购物车', 'page_name': 1, 'page_char': '购物车',
               'cartobj_list': cartobj_list,}

    if request.is_ajax():
        count = request.GET.get('count')
        print("count:", count)
        gid = int(request.GET.get('gid'))
        cartobj = models.Cart.objects.get(user_id=uid, good_id=gid)
        cartobj.count = count
        cartobj.save()
        return JsonResponse({'status': True})

    return render(request, 'cartinfo/cart.html', content)

@auth_login
def addcart(request, gid, cid): # cid: 数量
    gid = int(gid)
    cid = int(cid)
    uid = request.session.get('user_id')

    if request.method == 'GET':
        cartobj_list = models.Cart.objects.filter(user_id=uid, good_id=gid)
        if len(cartobj_list) >= 1: # 该用户已存在该商品id
            cartobj = cartobj_list[0]
            cartobj.count = cartobj.count + cid
        else:
            cartobj = models.Cart()  # 没有数据，创建一条
            cartobj.user_id = uid
            cartobj.good_id = gid
            cartobj.count = cid
        cartobj.save()

        # 如果是ajax请求，就执行：
        if request.is_ajax():
            # count = models.Cart.objects.filter(user_id=uid).aggregate(Count('count'))
            count = models.Cart.objects.filter(user_id=uid).count()
            return JsonResponse({'count': count})

        return redirect('/cart/')

def delcart(request, gid, cid):
    if request.method == 'GET':
        gid, cid = int(gid), int(cid)
        uid = request.session.get('user_id')
        cartobj = models.Cart.objects.get(user_id=uid, good_id=gid)
        if cartobj:
            cartobj.delete()
        ret = redirect('/cart/')
        return ret

# 第二种删除不刷新的方式
def delete(request, ctid):
    print(request.method)
    if request.method == 'GET':
        if request.is_ajax():
            try:
                print(type(ctid))
                cartobj = models.Cart.objects.get(pk=ctid)
                cartobj.delete()
                data = {'status': True}
            except Exception as e:
                print(e)
                data = {'status': False}
            return JsonResponse(data)
        return HttpResponse('ok')

@auth_login
def post_order(request):
    if request.method == 'GET':
        uid = request.session.get('user_id')
        cartobj_list = models.Cart.objects.filter(user_id=uid)
        userobj = UserInfo.objects.get(pk=uid)
        addr_dic = userobj.uaddrs.values('pro').first()  # 不可以接着写.get('pro')，这是在userobj对象下
        # print(addr_dic.get('pro'))

        content = {'title': '提交订单页', 'page_name': 1, 'page_char': '提交订单',
                   'cartobj_list': cartobj_list, 'addr': addr_dic.get('pro'),}

        return render(request, 'cartinfo/place_order.html', content)