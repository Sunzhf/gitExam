# -*- coding:utf-8 -*-
import datetime
import json


# 获取当前时间 年-月-日 时:分:秒
def get_time_now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 获取当前日期 年-月-日
def get_date_now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def json_loads(data):
    return json.loads(data)


def json_dumps(data):
    return json.dumps(data)


def get_username(request):
    return request.user.username


# DateTimeField格式化
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def datetime_cover_str(item):
    obj = {}
    if item.has_key('_id'):
        del item['_id']
    for k in item:
        if isinstance(item[k], datetime.datetime):
            obj[k] = item[k].strftime('%Y-%m-%d %H:%M:%S')
        else:
            obj = item
    return obj




def get_all_page_count(data_count, PAGE_SIZE):
    c = data_count / PAGE_SIZE if data_count % PAGE_SIZE == 0 else data_count / PAGE_SIZE + 1
    return 1 if c == 0 else c


def get_page_data(cursor, page_num=1, page_size=10):
    return cursor[(page_num - 1) * page_size: page_size * page_num]


def in_arr(key, value, arr):
    for x in arr:
        if x[key] == value:
            return True
    return False
