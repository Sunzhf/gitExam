# -*- coding: utf-8 -*-
from common.log import logger
import functools
from django.http import HttpResponse
import json


class try_exception(object):
    """
    decorator. log exception if task_definition has
    """

    def __init__(self, exception_return='', exception_desc='error', log=True):
        self.exception_desc = exception_desc
        self.exception_return = exception_return
        self.is_log = log

    def __call__(self, task_definition):
        @functools.wraps(task_definition)
        def wrapper(*args, **kwargs):
            try:
                return task_definition(*args, **kwargs)
            # except timeout.TimeoutError:
            #     raise
            except Exception as e:
                desc = '[{0}] {1}'.format(task_definition.func_name, self.exception_desc)
                if self.is_log:
                    logger.exception(u"%s: %s", desc, e)
                else:
                    logger.warning(u"%s: %s", desc, e)
                return HttpResponse(json.dumps({
                    'result': False,
                    'message': u'系统异常,请联系管理员!{0}'.format(e.message)
                    if not self.exception_return else u"{0}异常".format(self.exception_return)
                }))

        return wrapper
