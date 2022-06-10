from diskMap import DiskMap
import os
if __name__=="__main__":
    dm = DiskMap(".","HashMapName")
    for i in range(8000):
        print(i)
        dm.add(str(i),i)
    for i in range(5000,8000):
        dm.delete(str(i))
    for i in range(200):
        dm.delete(str(i))
    for i in range(8000,9000):
        dm.add(str(i),i+1000)
    for i in range(8000):
        print(dm.read(str(i)))
    print("size before shrink ", os.path.getsize(self.filePath)/BLOCK_SIZE)
    dm.shrink()
    print("size after shrink", os.path.getsize(self.filePath)/BLOCK_SIZE)
    dm.close()