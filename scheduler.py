from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", minutes=1, jitter=120)
def timed_job():
    exec(open("scraper.py").read())


exec(open("scraper.py").read())
scheduler.start()
