import collections

from db import fetchall , update


def def_value():
    return []

#
# # 같은 시간 앞, 뒤로 nginx, alb 로그들을 가져와 abnormal 을 판단한다.
# def process_abnormal(start, end):
#     nginx_sql = f"SELECT * FROM log WHERE timestamp >= '{start}' AND timestamp <= '{end}' AND datasource = 'nginx' ORDER BY timestamp ASC"
#     nginx = fetchall(nginx_sql)
#     nginx_dict = collections.defaultdict(def_value)
#     for n in nginx:
#         nginx_dict[n['timestamp']].append(n)
#
#     alb_sql = f"SELECT * FROM log WHERE timestamp >= '{start}' AND timestamp <= '{end}' AND datasource = 'alb' ORDER BY timestamp ASC"
#     alb = fetchall(alb_sql)
#     alb_dict = collections.defaultdict(def_value)
#     for a in alb:
#         alb_dict[a['timestamp']].append(a)
#
#     print(nginx_dict)
#     for a in alb_dict:
#         print(a)
#
#     # nginx 로그가 적을 것으로 생각되어 nginx 기준으로 시작한다.
#     # nginx timestamp 가 큰 것부터 작은 것 순으로
#     for tms in nginx_dict:
#         list = nginx_dict[tms]
#         for l in list:
#             # alb 로그랑 비교. 이때 현재 초 먼저 비교. 없을 경우 1초 전과 비교.
#
#             # if match
#                 # 해당 것 삭제
#             pass
#
#
# process_abnormal('2022-11-27 00:00:00', '2022-11-28 23:59:59')


def get_null_type_log():
    sql = "SELECT * FROM log_tb WHERE type IS NULL"
    null_type_log = fetchall(sql)
    log_dict = key_select(null_type_log)

    abnormal_log = []
    normal_log = []

    for key, value in log_dict.items():
        if(len(value) == 1):
            abnormal_log.append(value[0])
            pass

        if(len(value) == 2):
            alb = 0
            nginx = 0
            dt1 = 0
            dt2 = 1000
            for idx, val in enumerate(value):
                if(val['datasource'] == 'alb'):
                    alb = alb + 1
                    dt1 = val['timestamp']
                if (val['datasource'] == 'nginx'):
                    nginx = nginx + 1
                    dt2 = val['timestamp']
            if(alb==0 or nginx==0):
                abnormal_log.append(value[0])
                abnormal_log.append(value[1])
            else:
                td = (dt2-dt1)
                if(td.total_seconds() <= 1 and td.total_seconds()>=0):
                    normal_log.append(value[0])
                    normal_log.append(value[1])
                else:
                    abnormal_log.append(value[0])
                    abnormal_log.append(value[1])

        else:
            nginx_log = []
            alb_log=[]

            for i in value:
                if(i['datasource'] == 'nginx'):
                    nginx_log.append(i)
                if(i['datasource']=='alb'):
                    alb_log.append(i)

            for i_index, i_value in enumerate(alb_log):
                dt1 = i_value['timestamp']
                flag = False
                for j_index, j_value in enumerate(nginx_log):
                    dt2 = j_value['timestamp']
                    td = dt2-dt1
                    if(td.total_seconds() <= 1 and td.total_seconds()>=0):
                        normal_log.append(nginx_log.pop(j_index))
                        normal_log.append(i_value)
                        flag = True
                        break
                if(flag==False):
                    abnormal_log.append(i_value)

            for i in nginx_log:
                abnormal_log.append(i)

    save_normal(normal_log)
    save_abnormal(abnormal_log)



def save_abnormal(abnormal_logs):

    abnormal_set = []
    for i in abnormal_logs:
        uuid = i['uuid']
        abnormal_set.append(("abnormal",uuid))
    update(abnormal_set)


def save_normal(normal_logs):

    normal_set = []
    for i in normal_logs:
        uuid = i['uuid']
        normal_set.append(("normal",uuid))
    update(normal_set)


def key_select(logs):

    key_set = set()
    log_dict = {}

    for i in logs:
        key = key_generate(i)
        key_set.add(key)
        if key not in log_dict:
            log_dict[key] = [i]
        else:
            log_dict[key].append(i)


    return log_dict

    # for key, vlaue in log_dict.items():
    #     if(len(vlaue)>=3):
    #         print(" ")
    #         print(vlaue)

def key_generate(log):
    key = log['path'] + log['remote_addr'] + log['status'] + log['method'] + log['user_agent']
    return key


get_null_type_log()