# -*- coding: utf-8 -*-
# from django.http import HttpResponse
#
# def hello(request):
#     return HttpResponse("Hello, this is nice site!")

from django.shortcuts import render
from django.shortcuts import render_to_response

def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)

def change2log(request):
    request.encoding = 'utf-8'
    if 'login' in request.GET:
        return render_to_response('login2.html')

def change2adduser(request):
    request.encoding = 'utf-8'
    if 'adduser' in request.GET:
        return render_to_response('adduser.html')
