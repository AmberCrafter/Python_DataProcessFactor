print("Import modules, please wait...")
import schedule,time
# import threading
import datetime
import main

# lib module initialize
import os,sys,pandas,logging,json,numpy,logging,shutil

print("Import finish: "+str(datetime.datetime.now()))
# This is the simple way to do work in schedule.
# The best module is "APScheduler"

# schedule Referance: https://www.itread01.com/content/1544596032.html

def job():
    main.main()
    print(datetime.datetime.now())

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
