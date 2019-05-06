from datetime import datetime
import time,os,sys
try:
    from apscheduler.schedulers.background import BackgroundScheduler
except:
    import subprocess
    # import sys

    def install(package):
        subprocess.call([sys.executable, "-m", "pip", "install", package])

    install("apscheduler")

def tick():
    print('Tick: The time is:{0}'.format(datetime.now()))

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick,'interval',seconds=3) #間隔3秒鐘執行一次
    scheduler.start()  #這裡的排程任務是獨立的一個執行緒
    print('Press Ctrl {0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            # time.sleep(10)  #其他任務是獨立的執行緒執行
            # print('sleep!')
            print("Input 'stop' to exit this process.")
            txt=input()
            if txt=="stop":
                scheduler.shutdown()
                print('Exit The Job!')
                sys.exit()
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        print('Exit The Job!')