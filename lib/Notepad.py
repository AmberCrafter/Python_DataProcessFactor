class init:
    def __init__(self,dirfile):
        self.dirfile=dirfile
        pass
    def create(self,text):
        f=open(file=self.dirfile,mode='w')
        f.write(text)
        f.close()
    def append(self,text):
        f=open(file=self.dirfile,mode='a')
        f.write(text)
        f.close()