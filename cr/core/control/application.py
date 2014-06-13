#!/usr/bin/python
#encoding=UTF-8

from cr.core.datamodel.path import Path 
from cr.core.datamodel.dirdict import DirDict 
from cr.core.datamodel.inisetting import IniSetting
import os,shutil,sys
from baseapp import BaseApp,BaseAppBar
class Application(BaseApp):
	def __init__(self,path,globals={}):
		self.globals=globals
		self.initpath=os.path.join(path,'init.ini')
		self.path=Path(self.initpath,path)
		super(Application,self).__init__(path)
		self.execFile()
	def execFile(self):
		self.namespace_dic=dict([('env',DirDict(self.path['data']['env'])),('setting',IniSetting(self.path['data']['setting']))]+zip(self.globals.keys(),self.globals.values()))
		execfile(self.path['exec']['mainfile'].encode(sys.getfilesystemencoding()),self.namespace_dic)



class AppBar(BaseAppBar):
	def __init__(self,path,globals={}):
		super(AppBar,self).__init__(Application)
		self.path=path
		self.globals=globals
		self.update(self.path)
	def update(self,path):
		for i in os.listdir(path):
			self.load(os.path.join(path,i))
	def load(self,p):
		return super(AppBar,self).load(p,self.globals)
	def install(self,filename):
		return super(AppBar,self).install(filename,self.path,True)