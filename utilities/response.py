# -*- coding:utf-8 -*-
from common.mymako import render_json


# 成功返回数据
def success_result(data='', *args, **kwargs):
    result = {
        'result': True,
        'data': data
    }
    for arg in args:
        result = dict(result, **arg)
    result = dict(result, **kwargs)
    return render_json(result)


# 失败返回数据
def fail_result(message='', *args, **kwargs):
    if not message:
        message = u'系统异常,请联系管理员'
    result = {
        'result': False,
        'message': message
    }
    for arg in args:
        result = dict(result, **arg)
    result = dict(result, **kwargs)
    return render_json(result)
