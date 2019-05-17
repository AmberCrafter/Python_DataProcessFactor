import os,json

# Global Variables
root="../"
ConfigFilePath="../config/config.json"


def _createFolder(arg):
    os.mkdir(arg)

def _createConfig():
    # Default information
    config={
        "ConstantsTable":{
            "path":{
                "root":"~/",
                "config.json":"root/config/config.json",
                "temp":"root/temp",
                "OutputFolder":"root/output"
            },
            "parameter":{
                "ConfigFilePath":"../config/config.json",
                "TempFolder":"../temp/",
                "OutputFolder":"../output/"
            }
        },
        "Filter":{
            "FilterSettingFilePath":"../info/data_filter.txt",
            "NumberHeaders":24
        },
        "Backup": {
            "RawfilePath":"../data/",
            "RawfileList":[]
        },
        "Classifier":{
            "ClassifyMethod": "time",
            "OutputDataType": ["Rad","Aux"],
            "OutputFileType": ".dat",
            "OutputFileNameConnecter": "-",
            "RowOfHeaders":0
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
