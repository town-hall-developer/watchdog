import schedule
import time

import download_and_parse_alb
import download_and_parse_nginx

def job():
    print("I'm working...")
    download_and_parse_alb.run()
    download_and_parse_nginx.run()

schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)