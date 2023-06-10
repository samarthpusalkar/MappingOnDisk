# MappingOnDisk
An effort to make a map system which can be stored on hard disk/SSDs and other non voletile media.

## Usage

from mapD import MapD

create the hashed map file object
    md = MapD("HashMapName.md","path/to/file")

"HashMapName.mpd" is the name of the database file, it is created if it does not already exists and read otherwise
path/to/file is "." by default


Adding key-value pairs

md.add("key","value")

key and value are converted to string and then stored for current implementation


Reading value

md.read(str("key))

returns the value in string format, but it also appends with null dato to extend the value to BLOCK_SIZE for current implementation, need to resolve to returning only the required data in required dtype, but for now we can store and retrive in string format, and the data is contained in the initial characters of the string, user can use escape characters to mark the end of data while adding in string format and trim to that character when reading


Deleting value

md.delete(str(key))

deletes the key-value from datafile

md.shrink()

can be called to shrink datafile if some delete operations are performed, isn't called by default after delete operation.

