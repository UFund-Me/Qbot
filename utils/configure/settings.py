'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-02 00:12:18
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-09 23:29:18
FilePath: /Qbot/utils/configure/settings.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
'''
# -*-coding=utf-8-*-

import os
import json


def get_config_data(config_file='config.json'):
    json_file = os.path.join(os.path.dirname(__file__), config_file)
    with open(json_file, 'r', encoding='utf8') as f:
        _config = json.load(f)
        return _config


config = get_config_data()


def config_dict(*args):
    result = config
    for arg in args:
        try:
            result = result[arg]
        except:
            print('找不到对应的key')
            return None

    return result


class DBSelector(object):
    '''
    数据库选择类
    '''

    def __init__(self):
        self.json_data = config

    def config(self, db_type='mysql', local='qq'):
        db_dict = self.json_data[db_type][local]
        user = db_dict['user']
        password = db_dict['password']
        host = db_dict['host']
        port = db_dict['port']
        return (user, password, host, port)

    def get_engine(self, db, type_='qq'):
        from sqlalchemy import create_engine
        user, password, host, port = self.config(db_type='mysql', local=type_)
        try:
            engine = create_engine(
                'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(user, password, host, port, db))
        except Exception as e:
            print(e)
            return None
        return engine

    def get_mysql_conn(self, db, type_='qq',use_dict=False):
        import pymysql
        user, password, host, port = self.config(db_type='mysql', local=type_)
        try:
            if use_dict:
                conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8mb4',read_timeout=10,cursorclass= pymysql.cursors.DictCursor)
            else:
                conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8mb4',read_timeout=10)
        except Exception as e:
            print(e)
            return None
        else:
            return conn

    def mongo(self, location_type='qq', async_type=False):
        user, password, host, port = self.config('mongo', location_type)
        connect_uri = f'mongodb://{user}:{password}@{host}:{port}'
        if async_type:
            from motor.motor_asyncio import AsyncIOMotorClient
            client = AsyncIOMotorClient(connect_uri)
        else:
            import pymongo
            client = pymongo.MongoClient(connect_uri)
        return client


def get_tushare_pro():
    import xcsc_tushare as xc
    xc_token_pro = config.get('xc_token_pro')
    xc_server = config.get('xc_server')
    xc.set_token(xc_token_pro)
    pro = xc.pro_api(env='prd', server=xc_server)
    return pro


if __name__ == '__main__':
    pass