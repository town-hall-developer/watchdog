import schedule
import time

import download_and_parse_alb
import download_and_parse_nginx

import abnormal

def job():
    print("I'm working...")
    download_and_parse_alb.run()
    download_and_parse_nginx.run()

schedule.every(10).minutes.do(job)


def analysis_abnormal_job():
    print("I'm working...")
    abnormal.analysis_abnormal()

schedule.every(10).minutes.do(analysis_abnormal_job)

while True:
    schedule.run_pending()
    time.sleep(1)