# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from nicemodel.models import nuser

def login(request):
    request.encoding = 'utf-8'
    if 'pid' in request.GET and 'pwd' in request.GET:
        pid = request.GET['pid']
        password = request.GET['pwd']
        if len(nuser.objects.filter(pid=pid).filter(pwd=password)) > 0:
            # return render_to_response('controlpane.html')
            response = HttpResponseRedirect('/controlpane/')
            response.set_cookie('pid', pid, 3600)
            var1 = nuser.objects.get(pid=pid)
            response.set_cookie('prank', var1.rank, 3600)
            return response
        else:
            message = '用户名或密码错误'
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
