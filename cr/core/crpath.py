#!/usr/bin/python
#encoding=UTF-8

import os,UserDict,StringIO,sys,time
BuiltinFormatList=[(u"/",os.sep),
			(u"$HOME",os.environ[('HOME','HOMEPATH')[os.name=='nt']].decode(sys.getfilesystemencoding())),
			(u'$CWD',os.getcwdu())
			]
def getIntegralFormatList(parent_path):
	return [(u'$.',parent_path),]+BuiltinFormatList
def _format(s,d):
	return os.path.normpath(reduce(lambda x,y:x.replace(y,d[y]),[s]+d.keys()))
def format(p,parent_path=os.getcwdu()):
	return reduce(lambda x,y:x.replace(y[0],y[1]),[p]+getIntegralFormatList(parent_path))
def reformat(p,parent_path=os.getcwdu()):
	return reduce(lambda x,y:x.replace(y[1],y[0]),[p]+getIntegralFormatList(parent_path))