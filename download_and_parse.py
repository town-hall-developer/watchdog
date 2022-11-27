# s3://townhall-alb-bucket/AWSLogs/864493117148/elasticloadbalancing/ap-northeast-2/2022/11/27/864493117148_elasticloadbalancing_ap-northeast-2_app.townhall-lb.5fdaeebaccf886b1_20221127T1040Z_15.165.110.75_3gubphx9.log.gz
import os
import uuid
# from urlparse import urlparse

import boto3
import gzip
import re

BUCKET_NAME = 'townhall-alb-bucket'


def download_and_parse(object_name):
    print("processing...")
    print(object_name)
    file_name = object_name.split('/')[-1]
    s3 = boto3.client('s3')
    s3.download_file(BUCKET_NAME, object_name, file_name)

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
    response = s3.list_objects_v2(Bucket=bucket_name)
    return list(map(lambda obj: obj['Key'], response['Contents']))


def save_to_db(alb_log):
    sql = f'INSERT INTO `log_tb` (`uuid`, `timestamp`, `remote_addr`, `path`, `status`, `protocol`, `method`, `user_agent`, `datasource`) ' \
          f'VALUES ("{uuid.uuid4()}", "{alb_log.get("time")}", "{alb_log.get("client_ip")}", "path", "{alb_log.get("elb_status_code")}", "{alb_log.get("request_protocol")}", "{alb_log.get("request_type")}", "{alb_log.get("user_agent_browser")}", "abl");'

    print(sql)


# 아래와 같이 사용하면 됩니다.
#
# objs = list_objects(BUCKET_NAME)
# data = []
# for obj in objs:
#     if ".gz" not in obj:
#         continue
#     data.extend(download_and_parse(obj))


# objs = list_objects(BUCKET_NAME)
# data = []
# for obj in objs:
#     if ".gz" not in obj:
#         continue
#     data.extend(download_and_parse(obj))
#     break
#
# print(data)

tmp = {
    'type': 'h2',
    'time': '2022-11-26T12:16:07.038355Z',
    'elb': 'app/townhall-lb/5fdaeebaccf886b1',
    'client_ip': '117.110.83.195',
    'client_port': '60540',
    'target_ip': '10.0.2.154',
    'target_port': '80',
    'request_processing_time': '0.000',
    'target_processing_time': '0.002',
    'response_processing_time': '0.000',
    'elb_status_code': '204',
    'target_status_code': '204',
    'received_bytes': '1170',
    'sent_bytes': '1033',
    'request_type': 'OPTIONS',
    'request_url': 'https://api.townhall.place:443/socket.io/?EIO=4&transport=polling&t=OIptSNN',
    'request_protocol': 'HTTP/2.0',
    'user_agent_browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'ssl_cipher': 'ECDHE-RSA-AES128-GCM-SHA256',
    'ssl_protocol': 'TLSv1.2',
    'target_group_arn': 'arn:aws:elasticloadbalancing:ap-northeast-2:864493117148:targetgroup/haproxy-group/bd04dedbfee2c122',
    'trace_id': 'Root=1-63820387-751810ca0acda93d5dd74cef',
    'domain_name': 'api.townhall.place',
    'chosen_cert_arn': 'session-reused',
    'matched_rule_priority': '100',
    'request_creation_time': '2022-11-26T12:16:07.035000Z',
    'actions_executed': 'forward',
    'redirect_url': '-',
    'lambda_error_reason': '-',
    'target_port_list': '10.0.2.154:80',
    'target_status_code_list': '204',
    'classification': '-',
    'classification_reason': '-'
}

save_to_db(tmp)