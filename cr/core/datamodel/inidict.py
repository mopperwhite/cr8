#!/usr/bin/python
#encoding=UTF-8

from ConfigParser import ConfigParser
from UserDict import UserDict
class IniDict(UserDict,object):
	_getformater=None
	_setformater=None
	def __init__(self,fp='',encoding='utf-8'):
		UserDict.__init__(self)
		self.cp=ConfigParser()
		self.path=fp
		self.encoding=encoding
		if fp:self.load(self.path)
	def load(self,p=''):
		if not p:p=self.path
		self.cp.read(p)
		self.update(dict(map(lambda i:(i,dict(self.cp.items(i))),self.cp.sections())))
		if self._getformater:
			for i in self.keys():
				for j in self[i]:
					self[i][j]=self._getformater(self[i][j])
	def save(self,p=''):
		if not p:p=self.path
		for i in self.keys():
			if i not in self.cp.sections():
				i.add_section(i)
			for j in self[i].keys():
				if self._setformater:self.cp.set(i,j,self._setformater(self[i][j]))
				else:cp.set(i,j,self[i][j])
		self.cp.write(open(p,"w"))
	def addGetFormater(self,func):
		if self._getformater:self._getformater=lambda s:func(self._getformater(s))
		else:self._getformater=func
		self.load()
	def addSetFormater(self,func):
		if self._setformater:self._setformater=lambda s:self._setformater(func(s))
		else:self._setformater=func
		self.save()
