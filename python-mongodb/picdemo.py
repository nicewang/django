from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import *

def insertPic():
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    with open('Taipei.jpg','rb') as myimage:
        data = myimage.read()
        id = fs.put(data,filename='first_pic')
        print(id)
def getPic():
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    file = fs.get_version('first_pic', 0)
    data = file.read()
    out = open('Taipei_out.jpg','wb')
    out.write(data)
    out.close()
def delPic():
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    fs.delete(ObjectId('5a3a9e7ed3b8b60c234ff09f'))
def listName():
    client = MongoClient('localhost', 27017)
    db = client.Pic
    fs = GridFS(db, 'images')
    print(fs.list())
listName()
# insertPic()
# getPic()
# delPic()