import os,json

# Global Variables
root="../"
ConfigFilePath="../config/config.json"


def _createFolder(arg):
    os.mkdir(arg)

def _createConfig():
    # Default information
    config={
        "A Comment":{
            "0. ":"Constant Table only use to recode some information, not used in code.",
            "1. ":"Processing flow: initailize-->Backup-->Classifier(L0)-->DataQC(L1)"
        },
        "Backup": {
            "A Comment":"If FileList do not specify file, program will ask to weather want to backup all file in path or not.",
            "FileList": [], 
            "InputFolder": "../data/",
            "OutputFolder": "../temp/"
        }, 
        "Classifier": {
            "A Comment":"",
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
        }, 
        "ConstantsTable": {
            "A Comment":"",
            "parameter": {
                "ConfigFilePath": "../config/config.json", 
                "OutputFolder": "../output/", 
                "TempFolder": "../temp/"
            }, 
            "path": {
                "OutputFolder": "root/output/", 
                "config.json": "root/config/config.json", 
                "root": "~/", 
                "temp": "root/temp/"
            }
        }, 
        "Filter": {
            "A Comment":"",
            "FilterSettingFilePath": "../info/data_filter.txt", 
            "FilterCodeConfig":"../config/FilterCode.json",
            "NumberHeaders": 24
        },
        "DataQC":{
            "A Comment":"",
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
    }
    
    f=open(ConfigFilePath, 'w')
    json.dump(config, f, sort_keys=True, indent=4, separators=(', ', ': '))
    
def _basicFolderCheck():
    # not useful function.
    folderList=[
        "bin","config","lib"
    ]
    for element in folderList:
        filepath=root+element
        if not os.path.isdir(filepath):
            _createFolder(filepath)
            print("Create Folder '{0}'.({1})".format(element, filepath))
    print("Basic Folder Check Complet!")

def folderCheck(folderList):
    # folderList type = List
    for element in folderList:
        filepath=root+element
        if not os.path.isdir(filepath):
            _createFolder(filepath)
            print("Create Folder '{0}'.({1})".format(element, filepath))
    print("Folder Check Complet!")

def updateConfig(loseConfig):
    # lostConfig type = Dictionary
    f=open(ConfigFilePath, 'r')
    config=json.load(f)
    f.close()
    config.update(loseConfig)
    print(config)
    f=open(ConfigFilePath, 'w')
    json.dump(config, f, sort_keys=True, indent=4, separators=(', ', ': '))
    f.close()

def main():
    _basicFolderCheck()
    if not os.path.exists(ConfigFilePath):
        _createConfig()
    folderList=["data","temp","output"]
    folderCheck(folderList)

if __name__ == "__main__":
    main()
