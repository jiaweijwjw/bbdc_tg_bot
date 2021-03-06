from apscheduler.schedulers.blocking import BlockingScheduler


# this file is for automating the scaper file
scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", minutes=15, jitter=120)
def timed_job():
    exec(open("scraper.py").read())


exec(open("scraper.py").read())
scheduler.start()
