import json,os,sys,shutil
import numpy as np
import pandas as pd
import log
def _importConfig():
    ConfigFilePath="../config/config.json"
    try:
        f=open(ConfigFilePath)
    except FileNotFoundError:
        # _createConfig()
        # f=open(ConfigFilePath)
        print("Please Run the 'initailize.py' first!")
        raise("ConfigError")
    config=json.load(f)
    try:
        config=config['Backup']
    except:
        import initialize
        config={
            "A Comment":"If FileList do not specify file, program will ask to weather want to backup all file in path or not.",
            "FileList": [], 
            "InputFolder": "../data/",
            "OutputFolder": "../temp/"
        }
        initialize.updateConfig(config)
        print("""ErrorCode: 100\n
            Occurs: [backup.py]\n
            Please Setting the Classifer in config.json first. (../config/config.json)""")
        # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")

    if not os.path.isdir(config["OutputFolder"]):
        # _createFolder(config["OutputFolder"])
        print("Please Run the 'initailize.py' first!")
        raise Exception("ConfigError")
    return config

def copy_context(OutputFile,InputFile,StartRaw,EndRaw=None):
    # return recent position by StartRaw.
    # Check Outputfile exist or not.
    #if not os.path.isfile(OutputFile):
    f=open(file=InputFile,mode="r")
    header=""
    for i in range(4):
        header=header+f.readline()
    f.close()
    createFile(OutputFile,header)
    
    f=open(file=InputFile,mode="r")
    try:
        for i in range(StartRaw):
            f.readline()
    except:
        StartRaw=4
        for i in range(StartRaw):
            f.readline
    ff=open(file=OutputFile,mode='a')
    readin=f.readline()
    while readin:
        ff.write(readin)
        readin=f.readline()
        StartRaw+=1
    f.close()
    ff.close()
    return StartRaw
def createFile(OutputFile,txt):
    f=open(file=OutputFile,mode="w")
    f.write(txt)
    f.close()

def main():
    try:
        config=_importConfig()
        filepath=config['InputFolder']
    except Exception:
        print("Please Setting some information at config.json(Path:../config/config.json' )")
        raise

    finalFilePath=os.path.abspath(config["OutputFolder"])
    Logger=log.Logger("data_log")
    # print(Logger.getInfo().values.size == 0)
    if Logger.getInfo().values.size == 0:
        logInfo={
            "AuxRow":0,
            "RadRow":0
        }
    else:
        logInfo={
            "AuxRow":int(Logger.getInfo()["AuxRow"].values[0]),
            "RadRow":int(Logger.getInfo()["RadRow"].values[0])
        }
    if config['FileList'] == []:
        # Move All file to temp folder.
        print("Do you want to copy all file into temp folder? [Yes/No]")
        check=str(sys.stdin.readline()).replace("\n","").replace("\r","")  # check type is string
        if check.lower()=="yes":
            filelist=os.listdir(filepath)
            for element in filelist:
                # main process ====================================== #
                # print(element.find("Aux"))
                if element.find("Aux")!=-1:
                    FileType="AuxRow"
                elif element.find("Rad")!=-1:
                    FileType="RadRow"
                else:
                    FileType=-1
                    Logger.logging.critical("Not find correct filetype.")
                    sys.exit()
                InputFile=filepath+element
                OutputFile=finalFilePath+'\\'+element
                StartRaw=logInfo[FileType]
                if StartRaw<4:
                    StartRaw=4
                if os.path.isfile(OutputFile):
                    txt=""
                    f=open(file=InputFile,mode="r")
                    for i in range(4):
                        txt+f.readline()
                    createFile(OutputFile,txt)
                    f.close()
                StartRaw=copy_context(OutputFile,InputFile,StartRaw)
                logInfo[FileType]=StartRaw
                # =================================================== #
        else:
            pass
    else:
        for element in config['FileList']:
            # main process ====================================== #
            if element.find("Aux")!=-1:
                FileType="AuxRow"
            elif element.find("Rad")!=-1:
                FileType="RadRow"
            else:
                FileType=-1
                Logger.logging.critical("Not find correct filetype.")
                sys.exit()
            InputFile=filepath+element
            OutputFile=finalFilePath+'\\'+element
            StartRaw=logInfo[FileType]
            if StartRaw<4:
                StartRaw=4
            if os.path.isfile(OutputFile):
                txt=""
                f=open(file=InputFile,mode="r")
                for i in range(4):
                    txt+f.readline()
                createFile(OutputFile,txt)
                f.close()
            StartRaw=copy_context(OutputFile,InputFile,StartRaw)
            logInfo[FileType]=StartRaw
            # =================================================== #

    Logger.writeInfo("{0},{1}".format(logInfo["AuxRow"],logInfo["RadRow"]))

if __name__ == "__main__":
    main()