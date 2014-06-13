#!/usr/bin/python
#encoding=UTF-8

from cr.core import crzip,crtry
import traceback,shutil,os

class BaseApp(object):
	def __init__(self,path,id=''):
		self._path=path
		if not id:self.id=os.path.basename(path)
		else:self.id=id
	def pack(self,fp):
		crzip.pack(fp,self._path)
	def uninstall(self):
		shutil.rmtree(self._path)
		


class BaseAppBar(object):
	def __init__(self,app_class):
		self.list=[]
		self.app_class=app_class
	def load(self,*args,**kwargs):
		return self._load(*args,**kwargs)
	def _load(self,*args,**kwargs):
			app=crtry.run(self.app_class,*args,**kwargs)
			if app:self.list.append(app)
			return app
	def install(self,filename,targetdir,load=False):
		try:
			dir_=os.path.join(targetdir,os.path.splitext(os.path.split(filename)[1])[0])
			if not os.path.exists(dir_):
				os.mkdir(dir_)
			else:
				shutil.rmtree(dir_)
			crzip.unpack(filename,dir_)
			if load:
				return self.load(dir_)
			else:
				return dir_
		except:
			traceback.print_exc()
			return None
	def __iter__(self):
		return iter(self.list)