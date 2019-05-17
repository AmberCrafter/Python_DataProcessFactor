import json,os,sys

TempFolder="../temp/"

# def _createFolder(arg):
#     os.mkdir(arg)
# def _createConfig():
#     # Default information
#     configdata={
#         "Backup": {
#             "RawfilePath":"../data/",
#             "RawfileList":[]
#         }
#     }
    
#     filepath="../config/config.json"
#     f=open(filepath, 'w')
#     json.dump(configdata, f, sort_keys=True, indent=4, separators=(', ', ': '))

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
    config=config['Backup']

    if not os.path.isdir(TempFolder):
        # _createFolder(TempFolder)
        print("Please Run the 'initailize.py' first!")
        raise Exception("ConfigError")
    return config

def main():
    try:
        config=_importConfig()
        filepath=config['RawfilePath']
    except Exception:
        print("Please Setting some information at config.json(Path:../config/config.json' )")
        raise

    finalFilePath=os.path.abspath(TempFolder)
    if config['RawfileList'] == []:
        # Move All file to temp folder.
        print("Do you want to move all file into temp folder? [Yes/No]")
        check=str(sys.stdin.readline()).replace("\n","").replace("\r","")  # check type is string
        if check.lower()=="yes":
            filelist=os.listdir(filepath)
            for element in filelist:
                os.rename(filepath+element, finalFilePath+'\\'+element)
        else:
            pass
    else:
        for element in config['RawfileList']:
            os.rename(filepath+element, finalFilePath+'\\'+element)

if __name__=='__main__':
    main()