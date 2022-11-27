# s3://townhall-alb-bucket/AWSLogs/864493117148/elasticloadbalancing/ap-northeast-2/2022/11/27/864493117148_elasticloadbalancing_ap-northeast-2_app.townhall-lb.5fdaeebaccf886b1_20221127T1040Z_15.165.110.75_3gubphx9.log.gz
import os

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


# 아래와 같이 사용하면 됩니다.
#
# objs = list_objects(BUCKET_NAME)
# data = []
# for obj in objs:
#     if ".gz" not in obj:
#         continue
#     data.extend(download_and_parse(obj))

