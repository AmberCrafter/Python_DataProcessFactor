import os,json,logging
import pandas as pd

class Logger:
    def __init__(self,*logType):
        # logType: keyword under LogFile in config.json
        if logType!=():
            self.config=self._importConfig()
            self.config=self.config[logType[0]]
        else:
            self.config={
                "LogFilename":"../log/log.txt"
            }
        self._checkfile()
        self._setLogging()
        

    def _importConfig(self):
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
            config=config['LogFile']
        except:
            import initialize
            config={
                "LogFile":{
                    "A comment":"",
                    "LogFolder":"../log/",
                    "data_log":{
                        "LogFilename":"../log/data_log"
                    }
                }
            }
            initialize.updateConfig(config)
            print("""ErrorCode: 100\n
                Occurs: [backup_copy.py]\n
                Please Setting the Classifer in config.json first. (../config/config.json)""")
            # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")

        if not os.path.isdir(config["LogFolder"]):
            # _createFolder(config["OutputFolder"])
            print("Please Run the 'initailize.py' first!")
            raise Exception("ConfigError")
        return config
    def _setLogging(self):
        # logging.basicConfig(level=logging.DEBUG)
        LogFilename=self.config["LogFilename"]
        logging.basicConfig(level=logging.NOTSET,
            # format='%(asctime)s, %(name)-12s, %(levelname)-8s, %(message)s',
            format='%(asctime)s, %(levelname)-8s, %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=LogFilename)
    def _checkfile(self):
        if not os.path.isfile(self.config["LogFilename"]):
            f=open(file=self.config["LogFilename"],mode="w")
            txt="{0:19}, {1:8}, {2}\n".format("Time","Type","Information")
            f.write(txt)
        pass
    def writeInfo(self,information):
        logging.info(information)

    def getInfo(self):
        # This is the customize function
        df=pd.read_csv(self.config["LogFilename"],names=["Time","Type","AuxRow","RadRow"],skiprows=1)
        mask=df["Type"].str.strip()=="INFO"   # .str.strip() 用於清除空格
        # print(df[mask].tail(1)) 
        return df[mask].tail(1)

if __name__ == "__main__":
    logger=Logger("data_log")
    logger.getInfo()
    #logger.record("{0},{1}".format(1,2))