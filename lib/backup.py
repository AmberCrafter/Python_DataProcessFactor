import json,os,sys
import logging,shutil,time
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
def _isFileExist(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False
def _movefile(destfilepath, rawfilepath,count=0):
    if count>10:
        txt="The file \"{0}\" is been open, please close it first!".format(rawfilepath)
        print(txt)
        raise Exception(txt)
    try:
        if _isFileExist(destfilepath):  # 若目標位置文件存在，則先移除文件
            os.remove(destfilepath)
        # os.rename(rawfilepath, destfilepath)
        shutil.move(rawfilepath, destfilepath)
    except:
        count+=1
        time.sleep(1)
        _movefile(destfilepath, rawfilepath,count)
    

def main():
    try:
        config=_importConfig()
        filepath=config['InputFolder']
    except Exception:
        print("Please Setting some information at config.json(Path:../config/config.json' )")
        raise

    finalFilePath=os.path.abspath(config["OutputFolder"])
    # =============================================================== #
    # Logging setting
    # Create logger
    logger=logging.getLogger("backupLog")
    # Set logger handler, trigger level and formatter
    formation=logging.Formatter('%(asctime)-12s - %(levelname)-8s - [%(name)s] - %(message)s')
    handler=logging.FileHandler("../log/backup.log")
    handler.setFormatter(formation)
    logger.setLevel(logging.INFO)
    # Add handler into logger.
    logger.addHandler(handler)
    # =============================================================== #
    if config['FileList'] == []:
        # Move All file to temp folder.
        print("Do you want to copy all file into temp folder? [Yes/No]")
        check=str(sys.stdin.readline()).replace("\n","").replace("\r","")  # check type is string
        if check.lower()=="yes":
            filelist=os.listdir(filepath)
            if filelist==[]:
                logger.warning("File: No file exist!")
            else:
                for element in filelist:
                    destfilepath=finalFilePath+'\\'+element
                    rawfilepath=filepath+element
                    try:
                        _movefile(destfilepath, rawfilepath)
                        logger.info("File:\"{0}\" Backup successful!".format(element))
                    except Exception as err:
                        logger.warning(err.args[0])
                        pass
                    except:
                        logger.warning("Undefined Error occur!")
                        pass
                else:
                    pass
    else:
        for element in config['FileList']:
            if not _isFileExist(filepath+element):
                logger.warning("File:\"{0}\" is not exist!".format(element))
                continue
            destfilepath=finalFilePath+'\\'+element
            rawfilepath=filepath+element
            try:
                _movefile(destfilepath, rawfilepath)
                logger.info("File:{0} Backup successful!".format(element))
            except Exception as err:
                logger.warning(err.args[0])
                pass
            except:
                logger.warning("Undefined Error occur!")
                pass
            

if __name__ == "__main__":
    main()