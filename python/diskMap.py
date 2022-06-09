import os;
import mmap;
BLOCK_SIZE = 4096
class DiskMap:
    def __init__(self,path=".",name="test.dm"):
        self.file = None;
        self.filePath = os.path.join(path,name)
        if os.path.exists(os.path.join(path,name)):
            self.file = open(os.path.join(path,name),"r+");
            #self.file.write(0);
            return;
        os.makedirs(os.path.basename(path),exist_ok=True);
        self.file = open(self.filePath,"w+")
        self.file.write("0")
        self.file.flush()
        return;
    
    def add(self,key,value=None):
        if(not key):
            raise "Please Provide Key";
        hashID=DiskMap.hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return DiskMap.vtp(self.file, maxID, hashID, isWrite=True, data=value)
    
    def read(self,key):
        if(not key):
            raise "Please Provide Key";
        hashID=DiskMap.hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return DiskMap.vtp(self.file, maxID, hashID)

    def delete(self, key):
        if(not key):
            raise "Please Provide Key";
        hashID=DiskMap.hash(key)
        maxID = os.path.getsize(self.filePath)/BLOCK_SIZE
        return DiskMap.vtp(self.file, maxID, hashID, delete=True)
    def close(self):
        self.file.close()
        self.__del__()
    """def seekTo(self,key):
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
    """
    @staticmethod

    def hash(key):
        hashID = 0
        for char in key:
            hashID+=10*hashID+int(char)
        return hashID
            
    def vtp(fd, maxID, hashID, isWrite=False, data=0, delete=False):
        mod = 500
        inc = 250
        inc_change = 25
        phyAdr = hashID%(mod)
        blockSize = BLOCK_SIZE
        if(isWrite or delete):
            mm = mmap.mmap(fd.fileno(),0,prot=mmap.ACCESS_WRITE)
            while(mm[blockSize*phyAdr:blockSize*phyAdr+1].decode("utf-8")=="1"):
                fd.seek(phyAdr*blockSize+1)
                if str(hashID) == fd.read(len(str(hashID))):
                    break;  
                mod+=inc
                inc+=inc_change
                phyAdr = hashID%mod if (hashID>mod or not mm[blockSize*(hashID%mod):blockSize*(hashID%mod)+1]) else mod+1
                if mod>maxId:
                    end = (mod if (mod>phyAdr) else (phyAdr+1))
                    fd.seek(blockSize*end)
                    fd.write("0")
                    fd.flush()
                    mm.close()
                    mm = mmap.mmap(fd.fileno(),0,prot=mmap.ACCESS_WRITE)
                    maxID = end
            try:
                if(delete):
                    fd.seek(blockSize*phyAdr)
                    fd.write((blockSize)*"\0")
                    fd.flush()
                    mm.close()
                    return True
                else:
                    fd.seek(blockSize*phyAdr)
                    fd.write("1")
                    fd.seek(blockSize*phyAdr+1)
                    fd.write((blockSize-1)*"\0")
                    fd.seek(blockSize*phyAdr+1)
                    fd.write(str(hashID))
                    fd.write(str(data))
                    fd.flush()
            except:
                return None
            fd.seek(blockSize*phyAdr+1+len(str(hashID)))
            dataWritten = fd.read(blockSize-1-len(str(hashID)))
            mm.close()
            return dataWritten
        else:
            mm = mmap.mmap(fd.fileno(),0,prot=PROT_READ)
            while(True):
                fd.seek(phyAdr*blockSize+1)
                if str(hashID) == fd.read(len(str(hashID))):
                    break;  
                mod+=inc
                inc+=inc_change
                phyAdr = hashID%mod if (hashID>mod or not mm[blockSize*(hashID%mod):blockSize*(hashID%mod)+1]) else mod+1
                if mod>maxId:
                    mm.close()
                    return None
            fd.seek(blockSize*phyAdr+1+len(str(hashID)))
            dataRead = fd.read(blockSize-1-len(str(hashID)))
            mm.close()
            return dataRead
        
