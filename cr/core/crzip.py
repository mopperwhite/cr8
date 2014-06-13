#!/usr/bin/python
#encoding=UTF-8

import zipfile,os
def get_filenames_from_a_dir(dir):
    return reduce(lambda x,y:x+y,map(lambda p:map(lambda sp:(os.path.join(p[0],sp),os.path.join(p[0],sp)[len(dir):]),p[1]+p[2]), os.walk(dir)))
def pack(filename,dirname):
    z=zipfile.ZipFile(filename,'w')
    for i,j in get_filenames_from_a_dir(dirname):
	z.write(i,j)
def unpack(filename,dirname):
    if not os.path.exists(dirname):
	os.mkdir(dirname)
    z=zipfile.ZipFile(filename,'r')
    for i in z.namelist():
	if not os.path.exists(os.path.split(os.path.join(dirname,i))[0]):
	    os.mkdir(os.path.join(dirname,i))
	if os.path.split(os.path.join(dirname,i))[1]:
	    open(os.path.join(dirname,i),'w').write(z.read(i))
def namelist(filename):
    return zipfile.ZipFile(filename,'r').namelist()
class CRDirZip:
    def __init__(self,filename,dirname):
	self.filename=filename
	self.dirname=dirname
    def setfile(self,s):
	self.filename=s
    def setdir(self,s):
	self.dirname=s
    def Pack(self):
	pack(self.filename,self.dirname)
    def Unpack(self):
	unpack(self.filename,self.dirname)
    def NameList(self):
	namelist(self.filename)