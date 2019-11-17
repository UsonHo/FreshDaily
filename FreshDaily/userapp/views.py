from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from django.core.paginator import Paginator
import hashlib, json

from userapp import models
from goodsapp.models import GoodsInfo
from orderapp.models import OrderInfo
from cartapp.models import Cart

def auth_login(func):
    def warper(request, *args, **kwargs):
        # 两种可选
        # login_status = request.session.get('is_login')
        login_status = request.session.has_key('user_id')

        print("状态：", login_status)
        if not login_status:
            ret = redirect('/user/login/')
            # print("path:", request.path)
            # print("get_full_path:", request.get_full_path())
            # print("get_full_path_info:", request.get_full_path_info())

            # 仅适用于在被迫登录情况下获取登录前的url
            ret.set_cookie('url', request.get_full_path())
            return ret
        # uname = request.session.get('username')
        return func(request, *args, **kwargs)
    return warper
# @auth_login ==> uinfo = auth_login(uinfo)  ==>uinfo = warper()

# def index(request):
#     if request.method == 'GET':
#         return render(request, 'userinfo/index.html')

def register(request):
    if request.method == "GET":
        # autourl = reverse('user:register')
        # print(autourl)
        return render(request, "userinfo/register.html", {'title': "注册"})
    elif request.method == "POST":
        post = request.POST
        uname = post.get('user_name')
        upwd = post.get('pwd')
        ucpwd = post.get('cpwd')
        uemail = post.get('email')
        if ucpwd != upwd:
            return redirect('/user/register')
        m = hashlib.md5()
        m.update(upwd.encode('utf-8'))
        upwd = m.hexdigest()
        userobj = models.UserInfo.objects.create(uname=uname, upwd=upwd, uemail=uemail)
        models.Adress.objects.create(uaddrs_id=userobj.id, ushipaddrs_id=userobj.id)
        return redirect('/user/login')

def register_exist(request):
    if request.method == 'GET':
        uname = request.GET.get('uname')
        print(uname)
        name_exist = models.UserInfo.objects.filter(uname=uname).count() # 我们不关心用户的其他字段信息，获取个数即可
        data = {'name_exist': name_exist}
        return JsonResponse(data)

# 第一种方式可选（非本次使用的方式）
def login(request):
    if request.method == 'GET':
        print("method",request.method)

        username = request.COOKIES.get('username', '')
        username2 = request.session.get('username', '') # 仅做测试
        # 用于记住用户名，显示在表单上
        content = {'title': '登录', 'error_name':0, 'error_pwd': 0, 'uname': username or username2}
        ret = render(request, 'userinfo/login.html', content)

        if len(request.get_full_path()) > len(request.path_info):
            url = request.get_full_path().split('=')[1]
            ret.set_cookie('url', url)
        return ret

    elif request.method == 'POST':
        print("method：",request.method)
        post = request.POST
        username = post.get('username', None)
        pwd = post.get('pwd', None)

        m = hashlib.md5()
        m.update(pwd.encode('utf-8'))
        pwd = m.hexdigest()

        content = {'title': '登录', 'error_name':0, 'error_pwd': 0, 'uname': username}
        if username:
            userobj = models.UserInfo.objects.filter(uname=username).first()
            # print("userobj", userobj, userobj.upwd)
            if userobj:
                # 用户名正确
                if userobj.upwd == pwd:
                    rmb_uname = post.get('rmb_uname', 0)
                    prev_url = request.COOKIES.get('url', '/')
                    print("prev_url:", prev_url)
                    ret = HttpResponseRedirect(prev_url) # 跳转到登录前的页面
                    # 记住用户名
                    if rmb_uname:
                        ret.set_cookie('username', username)
                    else:
                        ret.set_cookie('username', username, max_age=10) # -1:立即失效
                    request.session['is_login'] = True
                    request.session['user_id'] = userobj.id
                    return ret

                content['error_pwd'] = 1
                return render(request, 'userinfo/login.html', content)
            content['error_name'] = 1
            return render(request, 'userinfo/login.html', content)
            # if userobj.upwd == pwd:
            #     rmb_uname = post.get('rmb_uname')
            #     # print("记住密码：", rmb_uname, type(rmb_uname))
            #     if rmb_uname:
            #         request.session['username'] = username
            #         request.session['is_login'] = True
            #     return redirect('/user/uinfo/')
        return redirect('/user/login/')


# 第二种方式可选(ajax)
def login_check(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print("username>>", username)
        if username:
            userobj = models.UserInfo.objects.filter(uname=username).first()
            print("userobj1", userobj)
            if not userobj:
                response = {'title': '登录', 'error_name': 1, 'error_pwd': 0, 'uname': username}
                return HttpResponse(json.dumps(response))
            pwd = request.POST.get('pwd')
            m = hashlib.md5()
            m.update(pwd.encode('utf-8'))
            pwd = m.hexdigest()
            if userobj.upwd == pwd:
                response = {'title': '登录', 'error_name': 0, 'error_pwd': 0, 'uname': username}
                return HttpResponse(json.dumps(response))
            response = {'title': '登录', 'error_name': 0, 'error_pwd': 1, 'uname': username}
            return HttpResponse(json.dumps(response))
        return redirect('/user/login/')

def login_check2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        m = hashlib.md5()
        m.update(pwd.encode('utf-8'))
        pwd = m.hexdigest()
        userobj = models.UserInfo.objects.filter(uname=username).first()
        if userobj:
            if userobj.upwd == pwd:
                rmb_uname = request.POST.get('rmb_uname', 0)
                url = request.COOKIES.get('url', '/')
                print("prev_url:", url)
                ret = HttpResponseRedirect(url)  # 跳转到登录前的页面
                if rmb_uname:
                    ret.set_cookie('username', username)  # 这里用cookie就可以了，是保存在用户浏览器端的
                request.session['is_login'] = True
                request.session['user_id'] = userobj.id
                request.session['username'] = username
                # return render(request, 'userinfo/login.html', {'status': True}) ajax提交，不能跳转的
                return ret # 通过任意表单方式实现提交
        # return render(request, 'userinfo/login.html', {'status': True}) ajax提交，不能跳转的
        return redirect('/user/login')

def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return JsonResponse({'status': True})

@auth_login
def uinfo(request):
    if request.method == 'GET':
        userobj = models.UserInfo.objects.get(id=request.session['user_id'])
        content = {'title': '用户中心',
                   'contact': userobj.uphone,
                   'uname': request.session.get('username'),
                   'email': userobj.uemail,
                   }

        # 获取最近浏览的商品
        goodids = request.COOKIES.get('lately_goodids', '') # ==>'6,4,3,8'
        goodid_list = goodids.split(',')
        # 根据id获取商品对象
        goodobj_list = []
        print("goodid_list", type(goodid_list), goodid_list)
        for goodid in goodid_list:
            if goodid:
                goodobj = GoodsInfo.objects.filter(id=int(goodid)).first()
                if goodobj:
                    goodobj_list.append(goodobj) # 严格按照列表顺序获取对象
        content['goodobj_list'] = goodobj_list

        return render(request, 'userinfo/user_center_info.html', content)

@auth_login
def uinfo_order(request):
    if request.method == 'GET':
        uid = request.session.get('user_id')

        # 获取该用户所有的订单信息
        order_objs = OrderInfo.objects.filter(user_id=uid).order_by('pk')
        # 再获取每个订单中的多个商品信息（即获取详单信息）==》user/uinfo_order/，由此决定设置怎么样的模型类

        # 分页操作
        # 1、创建Paginator对象
        pobj = Paginator(order_objs, 2)
        # 2、创建page对象
        pIndex = int(request.GET.get('pindex', '1'))
        order_objs = pobj.page(pIndex)
        print(order_objs.number)
        # 3、创建页码列表
        pagelist = pobj.page_range
        content = {
            'title': '全部订单',
            'order_objs': order_objs,
            'pagelist': pagelist,
        }

        return render(request, 'userinfo/user_center_order.html', content)

@auth_login
def uinfo_site(request):
    if request.method == 'GET':
        userobj = models.UserInfo.objects.filter(id=request.session['user_id'])
        content = {'addressee': userobj[0].recver, 'postal': userobj[0].upostal, 'phone': userobj[0].uphone}
        addr = userobj.values('uaddrs__pro')
        content['detailAddr'] = addr[0]['uaddrs__pro']
        content['title'] = '用户中心'
        return render(request, 'userinfo/user_center_site.html', content)

    elif request.method == 'POST':
        ''' 第一种方式ajax
            userobj = models.UserInfo.objects.get(id=request.session['user_id'])
            post = request.POST
            addressee = post.get('addressee')
            detailAddr = post.get('detailAddr')
            postal = post.get('postal')
            phone = post.get('phone')        
            models.Adress.objects.update(pro=detailAddr, uaddrs_id=userobj.id, ushipaddrs_id=userobj.id)
            dict = {'recver': addressee, 'upostal': postal, 'uphone': phone}
            models.UserInfo.objects.values().update(**dict)
            data = {'status': True}
            return HttpResponse(json.dumps(data))  # 记得dumps一下
        '''

        # 第二种方式
        userobj = models.UserInfo.objects.get(id=request.session['user_id'])
        post = request.POST
        userobj.recver = post.get('addressee')
        detailAddr = post.get('detailAddr')
        userobj.upostal = post.get('postal')
        userobj.uphone = post.get('phone')
        userobj.save()
        models.Adress.objects.filter(uaddrs_id=userobj.id).update(pro=detailAddr)
        return redirect('/user/uinfo_site')  # 可以把userobj传到前端，get/post简化
