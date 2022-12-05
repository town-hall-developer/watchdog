# s3://townhall-alb-bucket/AWSLogs/864493117148/elasticloadbalancing/ap-northeast-2/2022/11/27/864493117148_elasticloadbalancing_ap-northeast-2_app.townhall-lb.5fdaeebaccf886b1_20221127T1040Z_15.165.110.75_3gubphx9.log.gz
import os
import uuid
# from urlparse import urlparse
from urllib.parse import urlparse

import boto3
import gzip
import re

from db import insert, fetchall

ALB_BUCKET_NAME = 'townhall-alb-bucket'


def download_and_parse(object_name):
    print("processing...")
    print(object_name)
    file_name = object_name.split('/')[-1]
    s3 = boto3.client('s3')
    s3.download_file(ALB_BUCKET_NAME, object_name, file_name)

    fields = ["type",
              "time",
              "elb",
              "client_ip",
              "client_port",
              "target_ip",
              "target_port",
              "request_processing_time",
              "target_processing_time",
              "response_processing_time",
              "elb_status_code",
              "target_status_code",
              "received_bytes",
              "sent_bytes",
              "request_type",
              "request_url",
              "request_protocol",
              "user_agent_browser",
              "ssl_cipher",
              "ssl_protocol",
              "target_group_arn",
              "trace_id",
              "domain_name",
              "chosen_cert_arn",
              "matched_rule_priority",
              "request_creation_time",
              "actions_executed",
              "redirect_url",
              "lambda_error_reason",
              "target_port_list",
              "target_status_code_list",
              "classification",
              "classification_reason"]

    regex = r'([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \"([^ ]*) ([^ ]*) (- |[^ ]*)\" \"([^\"]*)\" ([A-Z0-9-]+) ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\" ([-.0-9]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^ ]*)\" \"([^\s]+?)\" \"([^\s]+)\" \"([^ ]*)\" \"([^ ]*)\"'

    resultArray = []

    with gzip.open(file_name, 'r') as log:
        lines = log.readlines()
        for line in lines:
            line = line.decode('utf-8')
            if 'health' in line:
                continue

            line_split = re.split(regex, line)
            line_split = line_split[1:len(line_split) - 1]
            resultDict = {}
            for i in range(len(fields)):
                resultDict[fields[i]] = line_split[i]

            resultArray.append(resultDict)

    os.remove(file_name)

    return resultArray


def list_objects(bucket_name):
    s3 = boto3.client('s3')
    # Create a reusable Paginator
    paginator = s3.get_paginator('list_objects_v2')

    # Create a PageIterator from the Paginator
    page_iterator = paginator.paginate(Bucket=bucket_name)

    re = []
    for page in page_iterator:
        re.append(list(map(lambda obj: obj['Key'], page['Contents'])))

    return re


def save_to_db(alb_log):
    netloc = urlparse(alb_log.get("request_url")).netloc
    path = alb_log.get("request_url").split(netloc)[1]
    date = alb_log.get("time").split('T')[0]
    time = alb_log.get("time").split('T')[1].replace('Z', '')
    sql = f'INSERT INTO `log_tb` (`uuid`, `timestamp`, `remote_addr`, `path`, `status`, `protocol`, `method`, `user_agent`, `datasource`) ' \
          f'VALUES ("{uuid.uuid4()}", "{date} {time}", "{alb_log.get("client_ip")}", "{path}", "{alb_log.get("elb_status_code")}", "{alb_log.get("request_protocol")}", "{alb_log.get("request_type")}", "{alb_log.get("user_agent_browser")}", "alb");'

    insert(sql)


def run():

    total = list_objects(ALB_BUCKET_NAME)
    object_list = set(total) - set(get_already_stored())
    print(f"alb: {object_list}")

    for object_name in object_list:
        if '.gz' not in object_name:
            continue
        datas = download_and_parse(object_name)
        for data in datas:
            save_to_db(data)

        sql = f'INSERT INTO `alb_log_file_tb` (`alb_log_file_name`) VALUES ("{object_name}")'
        insert(sql)



def get_already_stored():
    sql = 'SELECT alb_log_file_name FROM alb_log_file_tb'
    r = fetchall(sql)
    return list(map(lambda x: x['alb_log_file_name'], r))
