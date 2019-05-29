# ************************************************************** #
# Information:
# This process incoulding below:
#   1. Filting out specific time range config by "data_filter.txt"
#   2. Filting out "maintain data" with maintain code.
# ************************************************************** # 
import os,json
import datetime
# import pandas as pd
import datafilter_L1,Notepad,log

class DoQC:
    def __init__(self):
        def _importConfig():
            ConfigFilePath="../config/config.json"
            print(os.path.abspath(ConfigFilePath))
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
                        "A Comment": "In this level make the failed value into NullValue",
                        "OutputDataType": [
                            "Rad", 
                            "Aux"
                        ], 
                        "InputFolder": "../output/L0/", 
                        "OutputFolder": "../output/L1/", 
                        "OutputFileNameConnecter": "-", 
                        "OutputFileType": ".dat", 
                        "RowOfHeaders": 4,
                        "NullValue": -999,
                        "MaintainFlagHeader":"\"mt_flag_Tot\""
                    }
                }
                initialize.updateConfig(config)
                print("""ErrorCode: 100\n
                    Occurs: [dataQC.py]\n
                    Please Setting the Classifer in config.json first. (../config/config.json)""")
                # raise("ErrorCode: 100\nPlease Setting the Classifer in config.json first. (../config/config.json)")
            return config
        self.config = _importConfig()
    def drop_duplicates(self,filePath):
        # Old version; new version: self.reorganize
        # Failed===================================================== #
        # ff=open(filePath,"r")
        # txt=""
        # for i in range(4):
        #     txt=txt+ff.readline()
        # ff.close()
        # df = pd.read_csv(filePath,header=0,skiprows=[0,2,3])
        # df.drop_duplicates(subset="TIMESTAMP",keep="last",inplace=True)
        # ff=open("test.csv",'a+')
        # df.to_csv(ff,header=0,index=0)
        # =========================================================== #
        f=open(filePath,"r")
        txt=""
        for i in range(4):
            txt=txt+f.readline()
        readin=f.readline()
        formation="\"%Y-%m-%d %H:%M:%S\""           # time formation
        dummy="\"0001-01-01 00:00:00\""             # time initialize
        dummy=datetime.datetime.strptime(dummy,formation)
        while readin:
            readin=readin.replace("\n","").split(",")
            dummy1=datetime.datetime.strptime(readin[0],formation)
            print(dummy1)
            if dummy1>dummy:
                dummy=dummy1                        # get the first data witch is repeat.
                for i,val in enumerate(readin):
                    if i==0:
                        txt=txt+val
                        continue
                    txt=txt+","+val
                txt=txt+"\n"
            readin=f.readline()
        f.close()
        f=open(filePath,"w")
        f.write(txt)
        f.close()

    def reorganize(self,filePath):
        # Open Rawfile
        f=open(filePath,"r")
        txt=""
        for i in range(4):
            txt=txt+f.readline()
        readin=f.readline()

        # Generate timelist
        timelist=filePath.split("/")[-1][0:8]
        formation="%Y%m%d"
        timelist = datetime.datetime.strptime(timelist,formation)
        nummins=1440
        timelist = [timelist + datetime.timedelta(minutes=x) for x in range(0, nummins)]
        
        # Generate data list with timelist and number of columns.
        dummy = len(readin.replace("\n","").split(",")) # get number of columns.
        formation="\"%Y-%m-%d %H:%M:%S\""           # time formation
        # Bug formula------------------------------------------------ #
        # datatable=[[datetime.datetime.strftime(timelist[row],formation)]
        #     .extend([-999 for column in range(dummy-1)]) for row in range(nummins)]
        # ----------------------------------------------------------- #
        datatable=[[-999 for column in range(dummy)] for row in range(nummins)]
        for i,val in enumerate(timelist):
            datatable[i][0]=datetime.datetime.strftime(val,formation)

        # Create a datetime object to recode final time
        TimeRecode=datetime.datetime.strptime("\"0001-01-01 00:00:00\"",formation)
        while readin:
            readin=readin.replace("\n","").split(",")
            dummy=datetime.datetime.strptime(readin[0],formation)
            try:
                num=timelist.index(dummy)  # find the correct row in datatable.
            except:
                print("Failed to find: "+dummy)
                continue
            if dummy>TimeRecode:
                TimeRecode=dummy
            for i,val in enumerate(readin):
                datatable[num][i]=val
            readin=f.readline()
        f.close()

        # Write out Level1 data
        num=timelist.index(TimeRecode) # get the final time index
        for i in range(num+1):
            for j,val in enumerate(datatable[i]):
                if j==0:
                    txt=txt+str(val)
                    continue
                txt=txt+","+str(val)
            txt+="\n"
        f=open(filePath,"w")
        f.write(txt)
        f.close()

    def Level1(self,filelist=None):
        self.config = self.config["Level1"]
        InputFolder =self.config["InputFolder"]
        OutputFolder=self.config["OutputFolder"]
        if not os.path.isdir(OutputFolder):
            os.mkdir(OutputFolder)
        datafilter=datafilter_L1.filter().init()
        # print(datafilter.TimeInteval[0][3])
        # print(datafilter.FilterCodeConfig)
        
        typelist=self.config["OutputDataType"]
        typelist.append("Undefined")
        # filelist=os.listdir(InputFolder)
        if filelist==None:
            filelist=os.listdir(InputFolder)
        else:
            filelist=filelist
        for element in filelist:
            for dataType in typelist:
                # if all type befor Undifined not correct, then the type is Undefined
                if not -1==element.find(dataType):
                    break
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
            if os.path.isfile(OutputFilePath):
                ff=open(OutputFilePath,'r')

                # get number of row to start
                # Old method----------------------------------------- #
                # count=len(ff.readlines())
                # for i in range(count-self.config["RowOfHeaders"]):
                #     f.readline()
                # --------------------------------------------------- #
                # count: recode index of row in L0 file
                # dummy: recode L1 last time
                # dummy1:recode L0 current time
                readin =ff.readline()
                while readin:
                    dummy=readin
                    readin=ff.readline()
                ff.close()
                dummy=dummy.split(",")[0]
                formation="\"%Y-%m-%d %H:%M:%S\""  # time formation
                dummy=datetime.datetime.strptime(dummy,formation)

                readin=f.readline().split(",")[0]  # L0 file time to compare with L1 file last time
                dummy1=datetime.datetime.strptime(readin,formation)
                while not dummy==dummy1:
                    readin=f.readline().split(",")[0]  # L0 file time
                    dummy1=datetime.datetime.strptime(readin,formation)
            # else:
            #     count=self.config["RowOfHeaders"]     # count is not used

            while True:
                readin=f.readline()
                if not readin:
                    f.close()
                    break
                # ============================================== #
                # Process Data Filting
                readin = readin.replace("\n","").split(",")
                ## 1. data_filter.txt
                formation='"%Y-%m-%d %H:%M:%S"'
                datatime=datetime.datetime.strptime(readin[0],formation)
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
                if not os.path.isfile(OutputFilePath):
                    ff.create(header)
                ff.append(readin)
            # self.drop_duplicates(OutputFilePath)  # remove repeat value
            # ------------------------------------------------------- #
            # 1. Remove repeat value
            # 2. Patch lose value by -999
            self.reorganize(OutputFilePath)
            



if __name__ == "__main__":
    DoQC().Level1()
