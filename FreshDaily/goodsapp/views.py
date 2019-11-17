from django.shortcuts import render, HttpResponse
from goodsapp import models
from django.core.paginator import Paginator
from userapp.views import auth_login # 仅做页面登录跳转测试

from django.views import defaults

from cartapp.models import Cart

dic404 = {
    'guest_cart': 1,
    'title': '您访问的页面早已飞到地球之外'
}

def index(request):
    if request.method == 'GET':
        typelist = models.TypeInfo.objects.all()

        countobjs = Cart.objects.filter(user_id=request.session.get('user_id'))
        content = {'guest_cart': 1, 'index_clasify': 1, 'countobjs': countobjs}
        for i in range(len(typelist)):
            content['type' + str(i)] = typelist[0].goodsinfo_set.order_by('-id')[0:4]
            content['type' + str(i)*2] = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
        # print(content['type00'][0].id)
        content['title'] = '首页'
        return render(request, 'goodsinfo/index.html', content)

def list(request, tid, pid, oid):
    if request.method == 'GET':
        try:
            typeobj = models.TypeInfo.objects.get(id = int(tid))
        except Exception as e:
            print(e)
            # return defaults.bad_request(request, e, template_name='404.html')
            return render(request, '404.html', dic404)
        newgoods = typeobj.goodsinfo_set.order_by('-id')[0:2]
        if oid == '1': # 默认根据最新排序
            goodslist = models.GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        elif oid == '2': # 根据价格排序
            goodslist = models.GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
        elif oid == '3': # 根据点击量排序
            goodslist = models.GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
        else:
            goodslist = models.GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        paginator = Paginator(goodslist, 1) # 把本页商品对象列表传给分页对象实例化
        pageobjs = paginator.page(int(pid)) # 本页所有的商品对象列表
        content = {'guest_cart': 1,
                   'title': typeobj.ttitle+'商品列表页',
                   'extend_clasify': 1,
                   'extend_bread': 1,
                   'recomment': 1,
                   'newgoods': newgoods,
                   # 'goods': goodslist, 不用再传了
                   'pageobjs': pageobjs,
                   'tid': tid,
                   'oid': oid,}

        countobjs = Cart.objects.filter(user_id=request.session.get('user_id'))
        content['countobjs'] = countobjs
        return render(request, 'goodsinfo/list.html', content)

# @auth_login
def detail(request, gid):
    if request.method == 'GET':
        try:
            goodobj = models.GoodsInfo.objects.get(id=gid)
        except Exception as e:
            print(e)
            return render(request, '404.html', dic404)
        newgoods = goodobj.gtype.goodsinfo_set.order_by('-id')[0:2]

        countobjs = Cart.objects.filter(user_id=request.session.get('user_id'))

        # 商品点击次数加1
        goodobj.gclick = goodobj.gclick + 1
        goodobj.save()

        content = {#'title': goodobj.gtype.ttitle+'商品详情页',
                   'title': goodobj.gtitle + '详情页',
                   'recomment': 1, 'extend_bread': 1, 'extend_clasify': 1,
                   'guest_cart': 1, 'detail_bread': 1,
                   'newgoods': newgoods,
                   'goodobj': goodobj,
                   'countobjs': countobjs,}
        ret = render(request, 'goodsinfo/detail.html', content)

        # 新增：实现最近浏览的商品，用于用户中心
        goodids = request.COOKIES.get('lately_goodids', '') # 获取lately_goodids字符串
        goodobj_id = '%d'%goodobj.id   # 把商品id转成字符串
        if goodids != '':
            # 先将字符串用符号分割成列表,用于统计重复浏览的商品
            goodids_list = goodids.split(',')
            if goodids_list.count(goodobj_id) >= 1:
                goodids_list.remove(goodobj_id) # 删除原先的浏览商品id，更新本次id
            goodids_list.insert(0, goodobj_id)
            if len(goodids_list) >= 6:
                goodids_list.pop(5)
            goodids = ','.join(goodids_list)
        else:
            # 获取到的是空字符串
            goodids = goodobj_id # 把当前浏览的商品id给cookie
        ret.set_cookie('lately_goodids', goodids)

        return ret


# 全文检索
from haystack.views import SearchView
class FacetedSearchView(SearchView):
    def extra_context(self):
        content = super(FacetedSearchView, self).extra_context()
        content['guest_cart'] = 1
        content['extend_clasify'] = 1
        content['title'] = '天天生鲜网站搜索页'

        # 购物车数量更新
        countobjs = Cart.objects.filter(user_id=self.request.session.get('user_id'))
        content['countobjs'] = countobjs

        return content