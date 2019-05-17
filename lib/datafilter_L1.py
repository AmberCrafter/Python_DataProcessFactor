import json
from datetime import datetime
import initialization
class filter():
    def __init__(self):
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
                config=config['Filter']
            except:
                import initailize
                config={
                    "Filter":{
                        "FilterSettingFilePath": "../info/data_filter.txt", 
                        "FilterCodeFilePath":"../config/FilterCode.json",
                        "NumberHeaders": 24
                    }
                }
                initialization.updateConfig(config)
                print("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
                # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
            return config
        self.config = _importConfig()

    def _importfiltersetting(self):
        # FilterCodeConfig
        FilterCodeConfig=self.config["FilterCodeConfig"]
        f=open(FilterCodeConfig)
        FilterCodeConfig=json.load(f)
        self.FilterCodeConfig=FilterCodeConfig["Level1"]
        # FilterSetting
        FilterSettingFilePath=self.config["FilterSettingFilePath"]
        f=open(FilterSettingFilePath)
        ## Readout header
        for i in range(self.config["NumberHeaders"]):
            f.readline()
        timeinteval=[[],[]]
        flag=[]
        while True:
            readin=f.readline()
            if not readin:
                f.close()
                break
            readin=readin.replace("\n","").split(",")
            formation='"%Y-%m-%d %H:%M:%S"'

            timeinteval[0].append(datetime.strptime(readin[0],formation))
            timeinteval[1].append(datetime.strptime(readin[1],formation))
            flag.append(readin[2])
        self.TimeInteval=timeinteval
        self.flag=flag
    def init(self):
        self._importfiltersetting()
        return self

if __name__ == "__main__":
    ft=filter()
    ft.init()
    print(ft.TimeInteval[0][3])