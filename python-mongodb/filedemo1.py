#coding=utf-8
'''
Created on 2015-9-29

@author: Administrator
'''
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import *

def insertFile():
    client = MongoClient('localhost', 27017)
    db = client.File
    fs = GridFS(db, 'Files')
    with open('test.xlsx','rb') as myimage:
        data = myimage.read()
        id = fs.put(data,filename='first')
        print(id)
def getFile():
    client = MongoClient('localhost', 27017)
    db = client.File
    fs = GridFS(db, 'Files')
    file = fs.get_version('first', 0)
    data = file.read()
    out = open('test_out_1.xlsx','wb')
    out.write(data)
    out.close()
def delFile():
    client = MongoClient('localhost', 27017)
    db = client.File
    fs = GridFS(db, 'Files')
    fs.delete(ObjectId('560a531b0d4eae34a4edbfdd'))
def listName():
    client = MongoClient('localhost', 27017)
    db = client.File
    fs = GridFS(db, 'Files')
    print(fs.list())
listName()
# insertFile()
# getFile()