# -*- coding: utf-8 -*-
from django.http import HttpResponse
from nicemodel.models import nuser

# 数据库操作
def lookup(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = nuser.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = nuser.objects.filter(id=1)

    # 获取单个对象
    response3 = nuser.objects.get(id=1)

    # 限制返回的数据，相当于SQL中的OFFSET 0 LIMIT 2；
    nuser.objects.order_by('name')[0:2]

    # 数据排序
    nuser.objects.order_by("id")

    # 上面的方法可以连锁使用
    nuser.objects.filter(name="wxn").order_by("id")

    # 输出所有数据
    for var in list:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")
