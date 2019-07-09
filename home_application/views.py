# -*- coding: utf-8 -*-
from common.mymako import render_mako_context
from blueking.component.shortcuts import get_client_by_user
from utilities.response import *
from conf.default import APP_ID, APP_TOKEN
import json
from models import *
from common.mymako import render_json
import time
import xlrd
from utilities.jobman import JobMan


def home(request):
    return render_mako_context(request, '/home_application/home.html')


def demo(request):
    return render_mako_context(request, '/home_application/demo.html')


def chart(request):
    return render_mako_context(request, '/home_application/chart.html')


def search_business(request):
    client = get_client_by_user(request)
    params = {
        'bk_app_code': APP_ID,
        'bk_app_secret': APP_TOKEN,
        "bk_username": request.user.username,
    }
    res = client.cc.search_business(params)
    if not res['result']:
        return fail_result(res['message'])
    return success_result(res['data']['info'])


# 根据业务获取主机
def search_host_by_business(request):
    client = get_client_by_user(request)
    dict_data = json.loads(request.body)
    params = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "bk_biz_id": dict_data['bk_biz_id'],
        "condition": [
        ],
        "page": {
            "start": 0,
            "limit": 100,
        }
    }
    res = client.cc.search_host(params)
    infos = res['data']['info']
    info_list = []
    for info in infos[0:7]:
        host = info['host']
        dict = {
            'business_id': dict_data['bk_biz_id'],
            'ip': host['bk_host_innerip'],
            'sys_name': host['bk_os_name'],
            'host_name': host['bk_host_name'],
            'cloud_region': 'default area',
            'bk_cloud_id': host['bk_cloud_id'][0]['bk_obj_id'],
            'men': host['bk_mem'],
            'disk': host['bk_disk'],
            'cpu': host['bk_cpu'],
        }
        info_list.append(dict)
    return success_result(info_list)


def search_topu(request):
    id = request.GET['id']
    client = get_client_by_user(request.user.username)
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "bk_biz_id": id,
    }
    data = client.cc.search_biz_inst_topo(kwarg)
    return render_json({'result': True, 'data': data})


def search_host(request):
    id = request.GET['id']
    type = request.GET['type']
    client = get_client_by_user(request.user.username)
    conList = [
        {
            "bk_obj_id": "host",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "module",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "set",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "biz",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "object",
            "fields": [],
            "condition": []
        }
    ]
    condition = [
        {
            "field": "bk_" + type + "_id",
            "operator": "$eq",
            "value": int(id)
        }
    ]
    for item in conList:
        if (type == item['bk_obj_id']):
            item['condition'] = condition
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "condition": conList,
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
        "pattern": ""
    }
    data = client.cc.search_host(kwarg)
    return render_json({'result': True, 'data': data})


def topu_detail(request):
    client = get_client_by_user(request.user.username)
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "bk_obj_id": 'host',
    }
    data = client.cc.search_object_attribute(kwarg)
    return render_json({'result': True, 'data': data})


def create_task(request):
    data = json.loads(request.body)
    client = get_client_by_user(request.user.username)
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "bk_biz_id": data['biz_id'],
        "template_id": data['tem_id'],
        "name": data['name'],
        "constants": data['con']
    }
    data = client.sops.create_task(kwarg)
    return render_json({'result': True, 'data': data})


def get_task(request):
    biz_id = request.GET['biz_id']
    task_id = request.GET['task_id']
    client = get_client_by_user(request.user.username)
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "bk_biz_id": biz_id,
        "task_id": task_id
    }
    data = client.sops.get_task_status(kwarg)
    return render_json({'result': True, 'data': data})


def get_users(request):
    client = get_client_by_user(request.user.username)
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
    }
    data = client.bk_login.get_all_users(kwarg)
    return render_json({'result': True, 'data': data})


def test_la(request):
    client = get_client_by_user(request.user.username)
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "target_app_code": APP_ID,
        "fields": "bk_app_code;bk_app_name;introduction;creator;developer"
    }
    data = client.bk_paas.get_app_info(kwarg)
    return render_json({'result': True, 'data': data})


def compare_time(time1, time2):
    s_time = time.mktime(time.strptime(time1, '%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2, '%Y-%m-%d'))
    return int(s_time) - int(e_time)


def ecs_excel_export(request):
    try:
        name = 'ali%s.xlsx' % (time.time())
        file = open(name, 'wb')
        file.write(request.FILES['file'].read())
        file.close()
        id = request.POST["id"]
        data = xlrd.open_workbook(name)
        table = data.sheets()[0]
        nrows = table.nrows
        index_list = ['id', 'InstanceId', 'InstanceName', 'PrivateIpAddress', 'business']
        data_list = []
        for i in range(1, nrows):
            data_dict = {}
            table_row_value = table.row_values(i)
            for g in range(table_row_value.__len__()):
                data_dict[index_list[g]] = table_row_value[g]
            data_list.append(data_dict)
        # for item in data_list:
        # Students.objects.create(test_data_id=id, name=item["id"], type=item["InstanceId"],
        #                         score=item["InstanceName"],
        #                         result=item["PrivateIpAddress"], desc=item["business"])
        return render_json({'result': True})
    except Exception, e:
        print e
        return render_json({'result': False})


def get_top_data(request):
    client = get_client_by_user(request)
    params = {
        'bk_app_code': APP_ID,
        'bk_app_secret': APP_TOKEN,
        "bk_username": request.user.username,
    }
    res = client.cc.search_business(params)
    tree_list = []
    for item in res["data"]["info"]:
        kwarg = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": request.user.username,
            "bk_biz_id": item["bk_biz_id"],
        }
        data = client.cc.search_biz_inst_topo(kwarg)
        tree_list += data["data"]
    return render_json({"result": True, "data": tree_list})


def get_host_data(request):
    id = request.GET['id']
    type = request.GET['type']
    client = get_client_by_user(request.user.username)
    conList = [
        {
            "bk_obj_id": "host",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "module",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "set",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "biz",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "object",
            "fields": [],
            "condition": []
        }
    ]
    condition = [
        {
            "field": "bk_" + type + "_id",
            "operator": "$eq",
            "value": int(id)
        }
    ]
    for item in conList:
        if (type == item['bk_obj_id']):
            item['condition'] = condition
    kwarg = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": request.user.username,
        "condition": conList,
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
        "pattern": ""
    }
    data = client.cc.search_host(kwarg)
    re_list = []
    for child in data["data"]["info"]:
        kw = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": request.user.username,
            "bk_supplier_account": "0",
            "hosts": [
                {
                    "ip": child["host"]["bk_host_innerip"],
                    "bk_cloud_id": child["host"]["bk_cloud_id"][0]["bk_inst_id"]
                }
            ]
        }
        re_data = client.gse.get_agent_status(kw)
        child_data = {
            "ip": child["host"]["bk_host_innerip"],
            "cloud": child["host"]["bk_cloud_id"][0]["bk_inst_name"],
            "module": child["module"][0]["bk_module_name"],
            "agent": re_data["data"]["0:" + child["host"]["bk_host_innerip"]]["bk_agent_alive"]
        }
        re_list.append(child_data)
    return render_json({'result': True, "data": re_list})


def search_host_new(request):
    client = get_client_by_user(request)
    dict_data = json.loads(request.body)
    ip = json.loads(request.body)['ip']
    ip_list = ip.strip().split('\n')
    params = {
        "bk_username": request.user.username,
        "bk_biz_id": dict_data['biz'],
        "ip": {
            "data": ip_list,
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "page": {
            "start": 0,
            "limit": 100,
        }
    }
    res = client.cc.search_host(params)
    res_list = []
    for item in res["data"]["info"]:
        host = list(HostInfo.objects.filter(host_ip=item["host"]["bk_host_innerip"],
                                            biz_id=dict_data['biz']).values())
        monitor = list(
            MonitorHost.objects.filter(host_ip=item["host"]["bk_host_innerip"],
                                       biz_ip=dict_data['biz'], is_monitor=True).values())
        res_list.append({
            "biz": dict_data['biz'],
            "ip": item["host"]["bk_host_innerip"],
            "os": item["host"]["bk_os_name"],
            "host": item["host"]["bk_host_name"],
            "cloud": item["host"]["bk_cloud_id"][0]["bk_inst_name"],
            "mem": host[len(host) - 1]["host_mem"] if len(host) > 0 else "",
            "disk": host[len(host) - 1]["host_disk"] if len(host) > 0 else "",
            "cpu": host[len(host) - 1]["host_cpu"] if len(host) > 0 else "",
            "monitor": len(monitor) > 0
        })
    return render_json({'result': True, "data": res_list})


def host_performance(request):
    biz = request.GET["id"]
    ip = request.GET["bk_host_innerip"]
    job = JobMan()
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    host_list = [
        {
            'ip': ip,
            'bk_cloud_id': '0'
        }
    ]
    job_obj = {
        biz: [
            {
                "host": host_list,
                "script_content": """
                    #!/bin/bash
                    MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
                    DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
                    CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
                    DATE=$(date "+%Y-%m-%d %H:%M:%S")
                    echo -e "$DATE|$MEMORY|$DISK|$CPU"
                    """,
                "script_type": "1",
                "account": "root"
            }
        ]
    }
    job.execute(job_obj)
    status, content = job.get_log(ip)
    if not status:
        return fail_result("查询主机性能失败")
    s_list = content.split('|')
    HostInfo.objects.create(host_ip=ip, biz_id=biz, host_mem=s_list[1],
                            host_disk=s_list[2], host_cpu=s_list[3], create_time=today)
    r_data = {"mem": s_list[1], "disk": s_list[2], "cpu": s_list[3]}
    return success_result(r_data)
