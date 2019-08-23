import pdfkit
from pymongo import MongoClient

client = MongoClient("127.0.0.1",27017)
#   获取指定名称的数据库
db_mp = client.get_database('mp')
#   获取指定名称的集合
coll = db_mp.get_collection('python')
#   查询所有记录，并获取指定的
cur = coll.find({},{'_id':0,'title':1,'content_url':1})

for doc in cur:
    if len(doc['content_url']) >= 4:
        try:
            pdfkit.from_url(doc['content_url'],'pdf/{}.pdf'.format(doc['title']))
        except Exception as identifier:
            print('异常{}'.format(identifier))
        
    
    
