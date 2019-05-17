import os,json
import sys
import initialization,Notepad

# class classifier:
#     def __init__(self, fileObject):
#         self.fileObject=fileObject

#     def classify(self):
#         pass
        

class MethodProcess:
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
                config=config['Classifier']
            except:
                config={
                    "Classifier": {
                        "ClassifyMethod": "time", 
                        "OutputDataType": [
                            "Rad", 
                            "Aux"
                        ], 
                        "OutputFolder": "../output/L0/", 
                        "OutputFileNameConnecter": "-", 
                        "OutputFileType": ".dat", 
                        "RowOfHeaders": 4
                    }, 
                }
                initialization.updateConfig(config)
                print("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
                # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
            return config
        self.config = _importConfig()

    def time(self):
        TempFolder = "../temp/"
        OutputFolder=self.config["OutputFolder"]
        typelist=self.config["OutputDataType"]
        typelist.append("Undefined")
        filelist=os.listdir(TempFolder)
        if not os.path.isdir(OutputFolder):
            os.mkdir(OutputFolder)
        for element in filelist:
            for dataType in typelist:
                # if all type befor Undifined not correct, then the type is Undefined
                if not -1==element.find(dataType):
                    break
            filepath=TempFolder+element
            # Debug *******************************************
            #result=os.path.isfile(filepath)
            #print("{0} isfile:{1} ".format(element, result))
            # *************************************************
            if not os.path.isfile(filepath):
                break
            f=open(filepath,'r')
            header=""
            for i in range(self.config["RowOfHeaders"]):
                header=header+f.readline()
            count=self.config["RowOfHeaders"]
            while True:
                readin=f.readline()
                count+=1
                print(count)
                if not readin:
                    f.close()
                    break
                date=str(readin[1:5])+str(readin[6:8])+str(readin[9:11])
                OutputFilePath=OutputFolder+date+self.config["OutputFileNameConnecter"]\
                    +dataType+self.config['OutputFileType']
                ff=Notepad.init(OutputFilePath)
                if os.path.isfile(OutputFilePath):
                    ff.append(readin)
                else:
                    ff.create(header)
                    ff.append(readin)
            

if __name__ == "__main__":
    pass