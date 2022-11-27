import datetime
import os
import uuid

import boto3
import gzip
from datetime import timedelta

from db import insert, fetchall
from utils import datetime_to_str

ALB_BUCKET_NAME = 'townhall-nginx-bucket'


def download_and_parse(object_name):
    print("processing...")
    print(object_name)
    file_name = object_name.split('/')[-1]
    s3 = boto3.client('s3')
    s3.download_file(ALB_BUCKET_NAME, object_name, file_name)

    resultArray = []

    with gzip.open(file_name, 'r') as log:
        lines = log.readlines()
        for line in lines:
            line = line.decode('utf-8')
            if 'health' in line:
                continue

            line_split = line.split('[')
            first = line_split[0]
            second = line_split[1]

            resultDict = {}
            resultDict['remote_addr'] = first.split(' ')[0]

            time = second.split(']')[0].split(' ')[0]
            day = time.split('/')[0]
            month = time.split('/')[1]

            if month == 'Nov':
                month = 11
            elif month == 'Dec':
                month = 12
            elif month == 'Jan':
                month = 1
            elif month == 'Feb':
                month = 2
            # TODO: 나머지 달 추가

            year = time.split('/')[2].split(':')[0]
            hour = time.split('/')[2].split(':')[1]
            min = time.split('/')[2].split(':')[2]
            sec = time.split('/')[2].split(':')[3]

            dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec))
            dt = dt - timedelta(hours=9)

            resultDict['time'] = dt
            third = second.split(']')[1].split('"')

            method_path_protocol = third[1].split(' ')

            resultDict['method'] = method_path_protocol[0]
            resultDict['path'] = method_path_protocol[1]
            resultDict['protocol'] = method_path_protocol[2]
            resultDict['status'] = third[2].strip().split(' ')[0]

            resultDict['user_agent'] = third[5]
            http_x_forwarded_for = third[7]
            if ',' in http_x_forwarded_for:
                http_x_forwarded_for = http_x_forwarded_for.split(',')[0]
            resultDict['remote_addr'] = http_x_forwarded_for

            resultArray.append(resultDict)

    os.remove(file_name)

    return resultArray


def list_objects(bucket_name):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name)
    return list(map(lambda obj: obj['Key'], response['Contents']))


def save_to_db(nginx_log):
    dt = datetime_to_str(nginx_log.get("time"))
    sql = f'INSERT INTO `log_tb` (`uuid`, `timestamp`, `remote_addr`, `path`, `status`, `protocol`, `method`, `user_agent`, `datasource`) ' \
          f'VALUES ("{uuid.uuid4()}", "{dt}", "{nginx_log.get("remote_addr")}", "{nginx_log.get("path")}", "{nginx_log.get("status")}", "{nginx_log.get("protocol")}", "{nginx_log.get("method")}", "{nginx_log.get("user_agent")}", "nginx");'

    try:
        insert(sql)
    except:
        print(sql)


def run():
    total = list_objects(ALB_BUCKET_NAME)
    object_list = set(total) - set(get_already_stored())
    print(object_list)

    for object_name in object_list:
        if '.gz' not in object_name or 'access' not in object_name:
            continue
        datas = download_and_parse(object_name)
        for data in datas:
            save_to_db(data)

        sql = f'INSERT INTO `nginx_log_file_tb` (`nginx_log_file_name`) VALUES ("{object_name}")'
        insert(sql)



def get_already_stored():
    sql = 'SELECT nginx_log_file_name FROM nginx_log_file_tb'
    r = fetchall(sql)
    return list(map(lambda x: x['nginx_log_file_name'], r))


run()
