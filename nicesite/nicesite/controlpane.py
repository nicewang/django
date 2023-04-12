from django.http import HttpResponse
from django.shortcuts import render_to_response
from . import mongodb

def controlpane(request):
    pid = request.COOKIES.get('pid')
    prank = request.COOKIES.get('prank')
    response = render_to_response('controlpane.html',{'pid':pid})
    response.set_cookie('pid', pid, 3600)
    response.set_cookie('prank', prank, 3600)
    return response

def up(request):
    pid = request.COOKIES.get('pid')
    prank = request.COOKIES.get('prank')
    request.encoding = 'utf-8'
    if 'path' in request.GET and 'fid' in request.GET and 'fname' in request.GET and 'partition' in request.GET:
        db = mongodb.connectDB('localhost', 27017)
        path = request.GET['path']
        fid = request.GET['fid']
        fname = request.GET['fname']
        partition = request.GET['partition']
        result = mongodb.upFile(db,path,fid,fname,partition,pid,prank)
        message = result.getMessage()
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

def down(request):
    pid = request.COOKIES.get('pid')
    prank = request.COOKIES.get('prank')
    request.encoding = 'utf-8'
    if 'fid' in request.GET and 'path_out' in request.GET:
        db = mongodb.connectDB('localhost', 27017)
        path_out = request.GET['path_out']
        fid = request.GET['fid']
        result = mongodb.downFile(db,fid,pid,prank,path_out)
        message = result.getMessage()
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
