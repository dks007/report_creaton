#from datatime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from success_tool import schedulerJob

def start():
    schedulers = BackgroundScheduler()
    schedulers.add_job(schedulerJob.executeSchedulerJob, 'interval', seconds=20)
    schedulers.start()