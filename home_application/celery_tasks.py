# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
from celery.schedules import crontab
from celery.task import periodic_task
from celery import task
from models import *
from utilities.jobman import JobMan
import time


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def performance():
    host = list(MonitorHost.objects.filter(is_monitor=True).values())
    job = JobMan()
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for item in host:
        host_list = [
            {
                'ip': item["host_ip"],
                'bk_cloud_id': '0'
            }
        ]
        job_obj = {
            item["biz_ip"]: [
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
        status, content = job.get_log(item["host_ip"])
        s_list = content.split('|')
        HostInfo.objects.create(host_ip=item["host_ip"], biz_id=item["biz_ip"],
                                host_mem=s_list[1], host_disk=s_list[2],
                                host_cpu=s_list[3], create_time=today)
