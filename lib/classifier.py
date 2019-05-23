import os,json
import sys
import Notepad

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
                import initialize
                config={
                    "Classifier": {
                        "ClassifyMethod": "time", 
                        "InputFolder": "../temp/",
                        "OutputDataType": [
                            "Rad", 
                            "Aux"
                        ], 
                        "OutputFolder": "../output/L0/", 
                        "OutputFileNameConnecter": "-", 
                        "OutputFileType": ".dat", 
                        "RowOfHeaders": 4
                    }
                }
                initialize.updateConfig(config)
                print("""ErrorCode: 100\n
                    Occurs: [classifier.py]\n
                    Please Setting the Classifer in config.json first. (../config/config.json)""")
                # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
            return config
        self.config = _importConfig()

    def time(self):
        InputFolder = self.config["InputFolder"]
        OutputFolder=self.config["OutputFolder"]
        typelist=self.config["OutputDataType"]
        typelist.append("Undefined")
        filelist=os.listdir(InputFolder)
        if not os.path.isdir(OutputFolder):
            os.mkdir(OutputFolder)
        Outputfilelist={} # make the output filelist
        for element in filelist:
            for dataType in typelist:
                # if all type befor Undifined not correct, then the type is Undefined
                if not element.find(dataType)==-1:
                    break
            filepath=InputFolder+element
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
                # get the filename
                dummy=date+self.config["OutputFileNameConnecter"]\
                    +dataType+self.config['OutputFileType']
                OutputFilePath=OutputFolder+dummy
                ff=Notepad.init(OutputFilePath)
                if not os.path.isfile(OutputFilePath):
                    ff.create(header)
                ff.append(readin)
                Outputfilelist.update({}.fromkeys([dummy]))
        return list(Outputfilelist.keys())  # used to dataQC.Level1
                
if __name__ == "__main__":
    pass
