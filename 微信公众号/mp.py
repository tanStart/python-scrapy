import requests
import json
import time
from pymongo import MongoClient


# 地址
url = "https://mp.weixin.qq.com/mp/profile_ext"
# mongo配置
client = MongoClient('127.0.0.1',27017)             #   创建MongoDB的连接对象
mp_db = client.mp                                   #   指定mp数据库，不存在则自动创建
mp_content = mp_db.python                          #   指定集合，不存在则自动创建  



#   插入数据
def param_data(data,datetime):
    title = data['title']                                 # 标题
    digest = data['digest']                               # 摘要
    content_url = data['content_url']                     # 文章地址
    cover = data['cover']                                 # 封面图片
    mp_content.insert({
        'title':title,
        'digest':digest,
        'content_url':content_url,
        'cover':cover,
        'datetime':datetime
    })

    

def get_mp(biz,uin,key,index=0,count=10):
    #   偏移量
    offset = (index+1)*count
    #   请求参数
    params = {
        "__biz":biz,
        "uin":uin,
        "key":key,
        "offset":offset,
        "count":count,
        "f":"json",
        "action":"getmsg"
    }
    #   请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }

    resp = requests.get(url=url,params=params,headers=headers)
    if resp.status_code == 200:
        resp_json = resp.json()
        if resp_json.get('errmsg') == 'ok':
            can_msg_continue = resp_json['can_msg_continue']
            general_msg_list = json.loads(resp_json['general_msg_list'])
            msg_list = general_msg_list.get('list')
            for msg in msg_list:
                try:
                    app_msg_ext_info = msg['app_msg_ext_info']
                    datetime = time.localtime(msg['comm_msg_info']['datetime'])
                    datetime = time.strftime('%Y-%m-%d %H:%M:%S',datetime)            # 发布时间
                    is_multi = app_msg_ext_info['is_multi']

                    param_data(app_msg_ext_info,datetime)
                    
                    if is_multi == 1:
                        multi_app_msg_item_list = app_msg_ext_info.get('multi_app_msg_item_list')
                        for multi_app_msg_item in multi_app_msg_item_list:
                            param_data(multi_app_msg_item,datetime)
                            
                except Exception as identifier:
                    print('异常{}'.format(identifier))
                    pass
            
            #   是否有下一页
            if can_msg_continue == 1:
                return True
            else:
                return False
        else:
            print('获取文章失败...')
    else:
        print('无法连接公众号')
        return False

if __name__ == '__main__':
    biz = 'MzI5NDY1MjQzNA=='
    uin = 'MzQ0NjE0MTY5NQ=='
    key = '88a11e695c4dcad73ac184a51193c7e31f03312dddcc8e8f316dd8f231d40c3c9bdc6a05a18d331f47d5698ab7d4c2bf4e504ad7bd9dab98498fd437a7dff427a9708c76896396a807311191cdb34d9c'
    index = 0
    while True:
        print('开始提取公众号第{}页文章'.format(index+1))
        can_msg_continue_flag = get_mp(biz,uin,key,index)
        time.sleep(5)
        index += 1
        if not can_msg_continue_flag:
            print('公众号文章抓取结束....')
            break
          
