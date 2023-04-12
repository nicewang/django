from pymongo import MongoClient

# conn = MongoClient('127.0.0.1',27017)
# db = conn.mydb
# my_set = db.myset
#
# users=[{"name":"zhangsan","age":18},{"name":"lisi","age":20}]
# my_set.insert(users)

conn = MongoClient('mongodb://127.0.0.1:27017/try')
db = conn.mydb1
my_set = db.myset1

users=[{"name":"zhangsan1","age":18},{"name":"lisi1","age":20}]
my_set.insert(users)
