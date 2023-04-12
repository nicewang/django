# -*- coding: utf-8 -*-
from django.http import HttpResponse
from . import mongodb
import datetime
from nicemodel.models import nuser

def adduser(request):
    # adduser_mysql()
    request.encoding = 'utf-8'
    if 'pid' in request.GET and 'pname' in request.GET and 'prank' in request.GET:
        pid = request.GET['pid']
        pname = request.GET['pname']
        prank = request.GET['prank']
        result = adduser_mongo(pid,pname,prank)
        message = result.getMessage()
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

def adduser_mysql():
    add = nuser(name='wxn', pwd='wxn', rank=1)
    add.save()

# 数据库操作
def adduser_mongo(pid,pname,prank):
    db = mongodb.connectDB('localhost', 27017)
    return mongodb.addUser(db,pid,pname,prank,datetime.datetime.now())
