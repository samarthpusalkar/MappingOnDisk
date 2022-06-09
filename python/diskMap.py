import os;
import mmap;
BLOCK_SIZE = 4096
class DiskMap:
    def __init__(self,path=".",name="test.dm"):
        self.file = None;
        if os.path.exists(os.path.join(path,name)):
            self.file = open(os.path.join(path,name));
            #self.file.write(0);
            return;
        os.makedirs(os.path.basename(path),exist_ok=True);
        self.filePath = os.path.join(path,name)
        self.file = open(self.filePath);
        return;
    
    def add(self,key,value=None):
        if(!key):
            raise "Please Provide Key";
        hashID=hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return vtp(self.file, maxID, hashID, isWrite=True, data=value)
    
    def read(self,key):
        if(!key):
            raise "Please Provide Key";
        hashID=hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return vtp(self.file, maxID, hashID)

    def seekTo(self,key):
        self.file.seek(0);
        for i in range(len(key)):
            reqGroup = key[0:i]
            group = ""
            groupEndPos = 0
            while (group != reqGroup and group in reqGroup):
                self.file.seek(offset,1)
                groupEndPos=self.file.tell()
                self.file.seek(1,1)
                char = ""
                group = ""
                while(char!=","):
                    group+=char
                    char = self.file.read(1)
                offset = 0
                char = ""
                while(char!=","):
                    offset+=char
                    char = self.file.read(1)
                offset = int(offset)
            if(group!=reqGroup){
                self.file.seek(groupEndPos)
                self.addGroup(reqGroup)
            }

    @staticmethod

    def hash(key):
        hashId = 0
        for char in key:
            hashID+=10*hashId+int(char)
        return hashId
            
    def vtp(fd, maxID, hashID, isWrite=False, data=0):
        mod = 500
        inc = 250
        inc_change = 25
        phyAdr = hashID%(mod)
        blockSize = BLOCK_SIZE
        if(isWrite):
            mm = mmap.mmap(fd.fileno(),0,prot=PROT_WRITE)
            while(mm[blockSize*phyAdr:blockSize*phyAdr+1]):
                if str(hashID) == mm[blockSize*phyAdr+1:blockSize*(phyAdr)+blockSize].decode("utf-8")[:len(str(hashID))]:
                    break;  
                mod+=inc
                inc+=inc_change
                phyAdr = hashID%mod if (hashID>mod or not mm[blockSize*(hashID%mod):blockSize*(hashID%mod)+1]) else mod+1
                if mod>maxId:
                    end = (mod if (mod>phyAdr) else (phyAdr+1))
                    mm[blockSize*maxID:blockSize*end]=0
                    maxID = end
            mm[blockSize*phyAdr]=1
            mm[blockSize*phyAdr+1:]=bytes(str(data), 'utf-8')
            return mm[blockSize*phyAdr:blockSize*phyAdr+blockSize].decode("utf-8")
        else:
            mm = mmap.mmap(fd.fileno(),0,prot=PROT_READ)
            while(mm[blockSize*phyAdr:blockSize*phyAdr+1]):
                if str(hashID) == mm[blockSize*phyAdr+1:blockSize*(phyAdr)+blockSize].decode("utf-8")[:len(str(hashID))]:
                    break;  
                mod+=inc
                inc+=inc_change
                phyAdr = hashID%mod if (hashID>mod or not mm[blockSize*(hashID%mod):blockSize*(hashID%mod)+1]) else mod+1
                if mod>maxId:
                    return None
            return mm[blockSize*phyAdr:blockSize*phyAdr+blockSize].decode("utf-8")
                
        
