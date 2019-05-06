import json
import os

TempFolder="../temp/"

def _createFolder(arg):
    os.mkdir(arg)

def _initialize():
    ConfigFilePath="../config/config.json"
    f=open(ConfigFilePath)
    config=json.load(f)
    config=config['Backup']

    if not os.path.isdir(TempFolder):
        _createFolder(TempFolder)
    return config

def backup():
    config=_initialize()
    filepath=config['RawfilePath']
    finalFilePath=os.path.abspath(TempFolder)
    for element in config['RawfileList']:
        os.rename(filepath+element, finalFilePath+'\\'+element)

if __name__=='__main__':
    backup()