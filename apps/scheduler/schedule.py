import matplotlib.pyplot as plt
from crontab import CronTab

cron = CronTab(user='prashant')
for job in cron:
    print(job)
scraper_job = cron.new(command=' python3 /home/prashant/price\ tracker\ tool/scrap2.py')
scraper_job.minute.every(30)
alert_job=cron.new(command= 'python3 /home/prashant/price\ tracker\ tool/alert.py')
alert_job.minute.every(30)
cron.write()
