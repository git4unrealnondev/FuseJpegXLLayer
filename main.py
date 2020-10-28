#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import time

from fuse import FUSE, FuseOSError, Operations


class Passthrough(Operations):

    writing = False
    fileLoc = None
    filelist = []

    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def imageCompress(self, path):
        os.system("resources/jpeg-xl/build/tools/cjpegxl " + str(self._full_path(path)) + " " + str(self._full_path(path)) + ".jpegxl")
        return

    def imageDeCompress(self, path):
        print ("Decompress ", (self._full_path(path)), path)
        os.system("resources/jpeg-xl/build/tools/djpegxl " + str(path) + ".jpegxl" + " " + str(path))
        time.sleep(2)
        return
	## Custom Commands 4 Integration
	# =======================
    def fileWritten(self, path):
        if self.writing:
            print ("filewritten ", path.split("/"))
            #if (len (path.split("/")) < 3): # File Deletion Filtering
            print ("File has been Written @ ", self.fileLoc, path, self._full_path(path))
            print (str(self._full_path(path).split(".")))
            ext = self._full_path(path).split(".")[1]
            print (ext)
            if (ext == "png"):
                self.imageCompress(path)
            elif (ext == "jpg"):
                self.imageCompress(path)
        self.writing = False
        
    def rmFiles(self):
        print ("FileRMList ", self.filelist)
        for each in self.filelist:
            os.remove(each)
        self.filelist.clear()
        return
    def readFile(self, path):
        pass
        
    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        print ("getatt2 ", full_path,sys.argv[1] )
        if (self._full_path(path).split(".")[0] == sys.argv[1]):
            self.rmFiles()
        #if (os.path.isdir(full_path) and full_path != sys.argv[1]):
        #    full_path += ".jpegxl"
        if (len(self._full_path(path).split(".")) > 1):
            ext = self._full_path(path).split(".")[1]
            
            if not (os.path.exists(self._full_path(path).split(".")[0] + "." + self._full_path(path).split(".")[1])):
            	if (ext == "jpg" or ext == "png"):
            		full_path += ".jpegxl"
            	    	#print (ext)
        st = os.lstat(full_path)
        print ("sysarg", sys.argv[1])
        
        #print ("getatt3 ", full_path,sys.argv[1] )
        #print ("getattr ",dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid')))
        print (self._full_path(path).split("."))
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime','st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
       # return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime','st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        #print (dirents)
        for r in dirents:
        
            #try:
            if (len(r.split(".")) > 2):
                if (r.split(".")[2] == "jpegxl"):
                  yield r.split(".")[0] + "." + r.split(".")[1]
                print (self._full_path(path) + r)
                
            else:
                yield r
                
            #except IndexError:
                
            #    print (r, " is not a jpegxl file, readdir", r.split("."))

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        print (full_path.split("."))
        ext = self._full_path(path).split(".")[1]
        if (ext == "png" or ext == "jpg"):
            print ("I WAS OPENED")
            self.imageDeCompress(full_path)
      
            finalize = os.open(full_path, flags)
            self.filelist.append(str(self._full_path(path).split(".")[0] + "." + self._full_path(path).split(".")[1]))
            return finalize
            # Tryng to access a compressed file. Shall Un-Compress
            
        #if (full_path.split(".")[-1] == "jpegxl"):
        #    print ("OPening", full_path)
        return os.open(full_path, flags)
        #else:
        #    return flags

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        print ("Creating", self.root)
        print ()
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        print ("Reading",fh, offset, os.SEEK_SET, self.root)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        self.writing = True
        #print ("Writing", fh, offset, len(buf),os.SEEK_SET, self.root )
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        l = os.close(fh)
        self.fileWritten(path)
        return l

    def fsync(self, path, fdatasync, fh):
        print ("fsync")
        return self.flush(path, fh)


def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])

