from diskMap import DiskMap

if __name__=="__main__":
    dm = DiskMap(".","HashMapName")
    for i in range(8000):
        print(i)
        dm.add(str(i),i)
    for i in range(600):
        dm.delete(str(i))
    for i in range(7000,8000):
        dm.add(str(i),i+1000)
    for i in range(8000):
        print(dm.read(str(i)))