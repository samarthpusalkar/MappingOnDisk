from diskMap import DiskMap
import os
from diskMap import BLOCK_SIZE
if __name__=="__main__":
    dm = DiskMap(".","HashMapName")
    for i in range(8000):
        print(i)
        if str(i) not in dm.add(str(i),i):
            print("Failed at, ",i)
            raise "Addition Failed"
    for i in range(8000):
        if str(i) not in dm.read(str(i)):
            raise "Retrival Failed"
    for i in range(5000,8000):
        dm.delete(str(i))
    for i in range(5000,8000):
        if dm.read(str(i))!=None:
            raise "Delete Failed"
    for i in range(50):
        dm.delete(str(i))
    for i in range(50):
        if dm.read(str(i))!=None:
            raise "Delete Failed"
    for i in range(8000,9000):
        if str(i+1000) not in dm.add(str(i),i+1000):
            print("Failed at, ",i)
            raise "Addition Failed"
    for i in range(8000):
        print(dm.read(str(i)))
    print("size before shrink ", os.path.getsize(dm.filePath)/BLOCK_SIZE)
    dm.shrink()
    print("size after shrink", os.path.getsize(dm.filePath)/BLOCK_SIZE)
    dm.close()