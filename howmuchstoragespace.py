import os
import time
import sys

def imageDeCompress(path):
	#print ("Decompress ", (self._full_path(path)), path)
	os.system("resources/jpeg-xl/build/tools/djpegxl " + str(path) + ".jpegxl" + " " + str(path))
	return

result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(sys.argv[1]) for f in filenames if os.path.splitext(f)[1] == '.jpegxl']
for each in result:
	print (each)
	stri = []
	stri = each.split(".")
	imageDeCompress(stri[0] + "." + stri[1])
time.sleep(2)
fileSize = 0
fileSizeOne = 0
for each in result:
	fileSize += os.path.getsize(each)

resultOne = [os.path.join(dp, f) for dp, dn, filenames in os.walk(sys.argv[1]) for f in filenames if os.path.splitext(f)[1] == '.png' or os.path.splitext(f)[1] == '.jpg']

time.sleep(2)
for each in resultOne:
	fileSizeOne += os.path.getsize(each)
	
print ("FileSize", fileSize)
print ("DeCompressed", fileSizeOne)

for each in resultOne:
	os.remove(each)
