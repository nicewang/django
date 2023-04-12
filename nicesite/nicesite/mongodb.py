# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import *
import numpy as np
import datetime

# 连接mongodb数据库
def connectDB(host,port): # host='localhost' port=27017
    client = MongoClient(host, port)
    db = client.FileSys
    return db

# 添加用户
def addUser(db,pid,pname,prank,pdate):
    try:
        if db.PERSON.count({"PID":pid}) > 0:
            return Result(isSuccess=False,message="此用户之前已经添加过！")
        db.PERSON.insert({"PID":pid,"PNAME":pname,"PRANK":prank,"PDATE":pdate,
                          "UPFILES":[],"DOWNFILES":[]})
    except Exception:
        return Result(isSuccess=False,message="添加用户失败，未知错误！")
    return Result(isSuccess=True,message="添加用户成功！")

# 删除用户
def delUser(db,pid):
    try:
        if db.PERSON.count({"PID": pid}) <= 0:
            return Result(isSuccess=False,message="所需删除用户并不存在！")
        db.PERSON.remove({"PID":pid})
    except Exception:
        return Result(isSuccess=False,message="删除用户失败，未知错误！")
    return Result(isSuccess=True,message="删除用户ID为"+str(pid)+"的用户成功！")

# 上传文件
def upFile(db,path,fid,fname,partition,pid,prank):
    if db.DOC.count({"FID":fid}) > 0: # 说明此文件之前已经上传过了
        return Result(isSuccess=False,message="此文件之前已经上传，请不要重复上传！")
    else:
        f_id,result0 = insertFile(db,path,fid)
        date = datetime.datetime.now()
        result1 = insertDoc(db,fid,f_id,fname,partition,pid,prank,date)
        result2 = insertFlist(db,fid,fname,date,partition)
        result3 = insertPerson(db,pid,fid,date)
        if result0:
            message0 = "上传文件成功，"
        else:
            message0 = "上传文件失败，"
        if result1:
            message1 = "更新数据集合DOC成功，"
        else:
            message1 = "更新数据集合DOC失败，"
        if result2:
            message2 = "更新数据集合FLIST成功，"
        else:
            message2 = "更新数据集合FLIST失败，"
        if result3:
            message3 = "更新数据集合PERSON成功。"
        else:
            message3 = "更新数据集合PERSON失败。"
        if result0 and result1 and result2 and result3:
            isSuccess = True
        else:
            isSuccess = False
        return Result(isSuccess=isSuccess,message=message0+message1+message2+message3)

def insertFile(db,path,fid):
    try:
        fs = GridFS(db, 'FILE')
        with open(path,'rb') as myfile:
            data = myfile.read()
            id = fs.put(data,FID=fid)
    except Exception:
        return -1,False
    return id,True

def insertDoc(db,fid,f_id,fname,partition,pid,prank,date):
    try:
        db.DOC.insert({"FID":fid,"FNAME":fname,"DATE":date,"PARTITION":partition,"F_ID":f_id,
                   "FPERSON":[{"PID":pid,"OPRTIME":date,"PRANK":prank,"POPERATION":1}]})
    except Exception:
        return False
    return True

def insertFlist(db,fid,fname,date,partition):
    try:
        db.FLIST.insert({"FID":fid,"FNAME":fname,"DATE":date,"PARTITION":partition})
    except Exception:
        return False
    return True

def insertPerson(db,pid,fid,date):
    try:
        db.PERSON.update({"PID":pid},{"$push":{"UPFILES":{"FID":fid,"OPRTIME":date}}})
    except Exception:
        return False
    return True

# 下载文件
def downFile(db,fid,pid,prank,outpath):
    if db.DOC.count({"FID":fid}) <= 0: # 数据集合里并没有所需下载的文件
        return Result(isSuccess=False,message="在数据集合里未找到所需下载的文件！")
    else:
        date = datetime.datetime.now()
        result1 = getFile(db,fid,outpath)
        result2 = updateDoc(db,fid,pid,date,prank)
        result3 = updatePerson(db,pid,fid,date)
        if result1:
            message1 = "下载文件成功，"
        else:
            message1 = "下载文件失败，"
        if result2:
            message2 = "更新数据集合DOC成功，"
        else:
            message2 = "更新数据集合DOC失败，"
        if result3:
            message3 = "更新数据集合PERSON成功。"
        else:
            message3 = "更新数据集合PERSON失败。"
        if result1 and result2 and result3:
            isSuccess = True
        else:
            isSuccess = False
        return Result(isSuccess=isSuccess,message=message1+message2+message3)


def getFile(db,fid,outpath):
    try:
        fs = GridFS(db, 'FILE')
        file = fs.get_version(FID=fid)
        data = file.read()
        out = open(outpath,'wb')
        out.write(data)
        out.close()
    except Exception:
        return False
    return True

def updateDoc(db,fid,pid,date,prank):
    try:
        db.DOC.update({"FID":fid},{"$push":{"FPERSON":{"PID":pid,"OPRTIME":date,
                                                       "PRANK":prank,"POPERATION":2}}})
    except Exception:
        return False
    return True

def updatePerson(db,pid,fid,date):
    try:
        # if db.PERSON.find({"PID":pid,"DOWNFILES.FID":fid}): # 之前已经下载过，就更新一下操作时间就好
        #     db.PERSON.update({"PID":pid},{"$set":{"DOWNFILES":{"FID":fid,"OPRTIME":date}}})
        # else:
        #     db.PERSON.update({"PID":pid},{"$push":{"DOWNFILES":{"FID":fid,"OPRTIME":date}}})
        db.PERSON.update({"PID": pid}, {"$push": {"DOWNFILES": {"FID": fid, "OPRTIME": date}}})
    except Exception:
        return False
    return True

# 删除文件
def delFile(db,fid):
    if db.DOC.count({"FID":fid}) <= 0: # 所需删除文件并不存在
        return Result(isSuccess=False,message="所需删除文件并不存在！")
    else:
        result0 = delFile1(db,fid)
        result1 = delDoc(db,fid)
        result2 = delFlist(db,fid)
        result3 = delPerson(db,fid)
        if result0:
            message0 = "删除文件成功，"
        else:
            message0 = "删除文件失败，"
        if result1:
            message1 = "更新数据集合DOC成功，"
        else:
            message1 = "更新数据集合DOC失败，"
        if result2:
            message2 = "更新数据集合FLIST成功，"
        else:
            message2 = "更新数据集合FLIST失败，"
        if result3:
            message3 = "更新数据集合PERSON成功。"
        else:
            message3 = "更新数据集合PERSON失败。"
        if result0 and result1 and result2 and result3:
            isSuccess = True
        else:
            isSuccess = False
        return Result(isSuccess=isSuccess,message=message0+message1+message2+message3)

def delFile1(db,fid):
    try:
        fs = GridFS(db, 'FILE')
        result = db.FILE.files.find({"FID":fid})
        for e in result:
            fs.delete(e["_id"])
    except Exception:
        return False
    return True

def delDoc(db,fid):
    try:
        db.DOC.remove({"FID":fid})
    except Exception:
        return False
    return True

def delFlist(db,fid):
    try:
        db.FLIST.remove({"FID":fid})
    except Exception:
        return False
    return True

def delPerson(db,fid):
    try:
        db.PERSON.update({"UPFILES.FID":fid},{"$pull":{"UPFILES":{"FID": fid}}})
        result = db.PERSON.update({"DOWNFILES.FID":fid},{"$pull":{"DOWNFILES":{"FID":fid}}})
        for e in result:
            db.PERSON.update({"DOWNFILES.FID": fid}, {"$pull": {"DOWNFILES": {"FID": fid}}})
    except Exception:
        return False
    return True

# 获取文件列表
def listName(db):
    result = db.FLIST.find()
    list = []
    for e in result:
        fid = e["FID"]
        fname = e["FNAME"]
        date = e["DATE"]
        partition = e["PARTITION"]
        tmp = np.array([fid, fname, date, partition])
        list.append(tmp)
    return np.asarray(list)

class Result(object):
    def __init__(self,isSuccess,message):
        self.isSuccess = isSuccess
        self.message = message

    def print_message(self):
        print(self.message)

    def set_isSuccess(self,isSuccess):
        self.isSuccess = isSuccess

    def isSuccess(self):
        if self.isSuccess:
            return True
        else:
            return False

    def set_message(self,message):
        self.message = message

    def getMessage(self):
        return self.message

# db = connectDB('localhost', 27017)
# result = upFile(db=db,path='37组数据库试验概要设计.pptx',fid='000002',fname='37组数据库试验概要设计.pptx',
#        partition=0,pid="2",prank=1)

# result = addUser(db,4,"zy",0,datetime.datetime.now())
# result = delUser(db,1)

# result = downFile(db=db,fid="000001",pid=5,prank=0,outpath='2.xmind')

# result = delFile(db,"000002")

# print(result.getMessage())

# a = listName(db)
# print(a)
# for i in range(a.shape[0]):
#     fid = a[i][0]
#     fname = a[i][1]
#     date = a[i][2]
#     date = datetime.datetime.astimezone(date)
#     partition = a[i][3]
#     print(fid+' '+fname+' '+' '+' '+str(date)+' '+str(partition))
