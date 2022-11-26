import collections

from db import fetchall


def def_value():
    return []


# 같은 시간 앞, 뒤로 nginx, alb 로그들을 가져와 abnormal 을 판단한다.
def process_abnormal(start, end):
    nginx_sql = f"SELECT * FROM log WHERE timestamp >= '{start}' AND timestamp <= '{end}' AND datasource = 'nginx' ORDER BY timestamp ASC"
    nginx = fetchall(nginx_sql)
    nginx_dict = collections.defaultdict(def_value)
    for n in nginx:
        nginx_dict[n['timestamp']].append(n)

    alb_sql = f"SELECT * FROM log WHERE timestamp >= '{start}' AND timestamp <= '{end}' AND datasource = 'alb' ORDER BY timestamp ASC"
    alb = fetchall(alb_sql)
    alb_dict = collections.defaultdict(def_value)
    for a in alb:
        alb_dict[a['timestamp']].append(a)

    print(nginx_dict)
    for a in alb_dict:
        print(a)

    # nginx 로그가 적을 것으로 생각되어 nginx 기준으로 시작한다.
    # nginx timestamp 가 큰 것부터 작은 것 순으로
    for tms in nginx_dict:
        list = nginx_dict[tms]
        for l in list:
            # alb 로그랑 비교. 이때 현재 초 먼저 비교. 없을 경우 1초 전과 비교.

            # if match
                # 해당 것 삭제
            pass


process_abnormal('2022-11-27 00:00:00', '2022-11-28 23:59:59')
