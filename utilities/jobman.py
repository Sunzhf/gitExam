# -*- coding: utf-8 -*-
import Queue
import base64
import time
from esb.client import get_esb_client
from common.log import logger


class ScriptType(object):
    Shell = 1

    Bat = 2

    def __init__(self):
        pass


class JobMan(object):
    max_running_count = 20
    failed_list = []
    ip_log = {}

    def __init__(self):
        self.failed_list = []
        self.ip_log = {}

    def get_log(self, ip):
        if ip not in self.ip_log:
            return False, "IP{0}未执行作业，可能是IP未录入或Agent异常".format(ip)

        return self.ip_log[ip]["is_success"], self.ip_log[ip]["log_content"]

    def execute(self, app_jobs={}):
        """
            app_jobs example:

            {<app_id>: [{"host": [{"ip": "xxxx", "bk_cloud_id": <cloud_id>}], "script_content": "", "script_type":"", "account": "root"}]}

        """
        q = Queue.LifoQueue()
        for app_id, jobs in app_jobs.items():
            for job in jobs:
                q.put({"app_id": app_id, "job": job})

        running_jobs = []

        while not q.empty():

            if len(running_jobs) > self.max_running_count:
                finished_jobs_tmp = []
                time.sleep(10)
                for running_job in running_jobs:
                    res, log_data = self.__get_log(running_job["job_inst_id"], running_job["app_id"])
                    if res:
                        finished_jobs_tmp.append(running_job)

                for finished_job in finished_jobs_tmp:
                    running_jobs.remove(finished_job)

                continue

            app_job = q.get()
            esb_client = get_esb_client()
            if "script_param" in app_job['job']:
                script_param = app_job['job']['script_param']
            else:
                script_param = ''
            res = esb_client.call('job', 'fast_execute_script', bk_biz_id=app_job["app_id"],
                                  script_content=base64.b64encode(app_job["job"]["script_content"]),
                                  script_type=app_job["job"]["script_type"], account=app_job["job"]["account"],
                                  ip_list=app_job["job"]["host"], script_param=script_param)
            if res['result']:
                task_instance_id = res['data']['job_instance_id']
                running_jobs.append({"app_id": app_job["app_id"], "job_inst_id": task_instance_id})
            else:
                err_msg = (u'fast_execute_script fail，error_msg: %s' % res['message'].decode("utf-8")).encode("utf-8")
                logger.error(err_msg)
                self.failed_list.append({
                    "host": app_job["job"]["host"],
                    "err_msg": err_msg
                })

        i = 0

        # while len(running_jobs) > 0 and i < 1440:
        while len(running_jobs) > 0 and i < 60:
            finished_jobs_tmp = []
            time.sleep(5)
            i += 1
            for running_job in running_jobs:
                res, message = self.__get_log(running_job["job_inst_id"], running_job["app_id"])
                if res:
                    finished_jobs_tmp.append(running_job)

            for finished_job in finished_jobs_tmp:
                running_jobs.remove(finished_job)

    def __get_log(self, task_instance_id, app_id):
        esb_client = get_esb_client()
        res = esb_client.call('job', 'get_job_instance_log', bk_biz_id=app_id, job_instance_id=task_instance_id,
                              username='admin')
        if res['result']:
            step = res['data'][0]
            if step['is_finished']:
                return self.__get_step_log(step)
            else:
                return False, None
        else:
            return False, None

    def __get_step_log(self, step):
        return_ip_content = []
        for step_res in step['step_results']:
            for ip_content in step_res['ip_logs']:
                if ip_content['ip'] in self.ip_log:
                    logger.error(ip_content['ip'] + " occurs repeat error when executing job!")
                    continue

                self.ip_log[ip_content['ip']] = {"is_success": step_res["ip_status"] == 9,
                                                 "source": ip_content['bk_cloud_id'],
                                                 "ip": ip_content['ip'],
                                                 "log_content": ip_content['log_content']}
        return True, None
