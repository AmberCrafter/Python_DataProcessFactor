import schedule,time
# import threading
import datetime
import main

# This is the simple way to do work in schedule.
# The best module is "APScheduler"

# schedule Referance: https://www.itread01.com/content/1544596032.html

def job():
    main.main()

def run():
    # Work flow without threading: 
    #   Open threading and setting-->
    #   do schedule job (if used 10s)
    #   wait a minute (70s after job start, it mean count a minute after job finish.)
    #   do next schedule job
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
run()
