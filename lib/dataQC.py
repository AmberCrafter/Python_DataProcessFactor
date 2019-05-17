# ************************************************************** #
# Information:
# This process incoulding below:
#   1. Filting out specific time range config by "data_filter.txt"
#   2. Filting out "maintain data" with maintain code.
# ************************************************************** # 
import os,json
from datetime import datetime

class DoQC:
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
                config=config['DataQC']
            except:
                import initialize
                config={
                    "Level1":{
                        "Comment": "In this level make the failed value into NullValue",
                        "OutputDataType": [
                            "Rad", 
                            "Aux"
                        ], 
                        "InputFolder": "../output/L0/", 
                        "OutputFolder": "../output/L1/", 
                        "OutputFileNameConnecter": "-", 
                        "OutputFileType": ".dat", 
                        "RowOfHeaders": 4,
                        "NullValue": -999
                    }
                }
                initialize.updateConfig(config)
                print("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
                # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
            return config
        self.config = _importConfig()

    def Level1(self):
        import datafilter_L1,Notepad
        self.config = self.config["Level1"]
        InputFolder=self.config["InputFolder"]
        OutputFolder=self.config["OutputFolder"]
        if not os.path.isdir(OutputFolder):
            os.mkdir(OutputFolder)
        datafilter=datafilter_L1.filter().init()
        # print(datafilter.TimeInteval[0][3])
        # print(datafilter.FilterCodeConfig)

        typelist=self.config["OutputDataType"]
        typelist.append("Undefined")
        filelist=os.listdir(InputFolder)
        for element in filelist:
            # for dataType in typelist:
            #     # if all type befor Undifined not correct, then the type is Undefined
            #     if not -1==element.find(dataType):
            #         break
            filepath=InputFolder+element
            OutputFilePath=OutputFolder+element
            # Debug *******************************************
            #result=os.path.isfile(filepath)
            #print("{0} isfile:{1} ".format(element, result))
            # *************************************************
            if not os.path.isfile(filepath):
                break
            f=open(filepath,'r')
            header=""
            for i in range(self.config["RowOfHeaders"]):
                readin=f.readline()
                header=header+readin
                if i==1:
                    columnHeader=readin.split(",")
                    mtFlagIndex=columnHeader.index(self.config["MaintainFlagHeader"])
            # print(mtFlagIndex)
            count=self.config["RowOfHeaders"]
            while True:
                readin=f.readline()
                count+=1
                print(count)
                if count==550:
                    print("stop")
                    pass
                if not readin:
                    f.close()
                    break
                # ============================================== #
                # Process Data Filting
                readin = readin.replace("\n","").split(",")
                ## 1. data_filter.txt
                formation='"%Y-%m-%d %H:%M:%S"'
                datatime=datetime.strptime(readin[0],formation)
                filterList=[]
                M1=False
                for i in range(len(datafilter.TimeInteval[0])):
                    starttime=datafilter.TimeInteval[0][i]
                    endtime=datafilter.TimeInteval[1][i]
                    M1=(starttime<datatime<endtime)
                    if M1==True:
                        filterList.extend(datafilter.FilterCodeConfig[str(datafilter.flag[i])])
                M1=len(filterList)>0    # Determine weather filterList empty or not. If not then M1=True.
                ## 2. MaintainCode
                M2=False
                if readin[mtFlagIndex]!="0":
                    # print(readin[mtFlagIndex])
                    filterList.extend(datafilter.FilterCodeConfig['1'])  # [1]: Imply ALL DATA replace into Null value.
                    M2=True
                if M1|M2:
                    filterList=list(set(filterList))
                    filtColumnList=[]
                    for i in range(3,len(readin)):
                        for element in filterList:
                            if columnHeader[i].find(element)!=-1:
                                filtColumnList.append(i)
                    for i in filtColumnList:
                        readin[i]="-999"
                    # print(readin)
                txt=""
                for i,val in enumerate(readin):
                    if i==0:
                        txt=val
                        continue
                    txt=txt+","+val
                readin=txt+"\n"
                # ============================================== #
                ff=Notepad.init(OutputFilePath)
                if os.path.isfile(OutputFilePath):
                    ff.append(readin)
                else:
                    ff.create(header)
                    ff.append(readin)


if __name__ == "__main__":
    DoQC().Level1()