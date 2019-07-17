import sys,os
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__)+"/../lib")
# sys.path.append("../lib/")
import initialize,backup,classifier,dataQC

def main():
    print("Initializing...")
    initialize.main()
    # print("Please check the config setting...")
    # print("Setting Done? [Yes/No]")
    # check=str(sys.stdin.readline()).replace("\n","").replace("\r","")  # check type is string
    # if not check.lower()=="yes":
    #     print("Please goto '../config/config.json check the setting.'")
    #     sys.exit(100)

    print("Backup the data, please wait...")
    backup.main()
    print("Backup done.")

    print("L0: Classifying Data....")
    filelist=classifier.MethodProcess().time()
    print("L0: Classify Done")

    print("L1: Quality Control of Data....")
    dataQC.DoQC().Level1(filelist)
    # dataQC.DoQC().Level1()
    print("L1: QC Done")
if __name__ == "__main__":
    main()
