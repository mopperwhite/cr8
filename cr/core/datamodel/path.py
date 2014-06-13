#!/usr/bin/python
#encoding=UTF-8

from inidict import IniDict
from cr.core import crpath
class Path(IniDict):
	def __init__(self,filename,parent_path=''):
		super(Path,self).__init__(filename)
		self.parent_path=parent_path
		self.addGetFormater(self.formater)
		self.addSetFormater(self.reformater)
	def formater(self,s):
		if self.parent_path:return crpath.format(s,self.parent_path)
		else:return crpath.format(s)
	def reformater(self,s):
		if self.parent_path:return crpath.reformat(s,self.parent_path)
		else:return crpath.reformat(s)


