#!/usr/bin/python
#encoding=UTF-8

from lineslist import LinesList
import os
from cr.core import crpath
class LinesPath(LinesList):
	def __init__(self,filename='',parent_path=os.getcwdu(),encoding='utf-8',linesep='\n'):
		self.parent_path=parent_path
		super(Paths,self).__init__(filename,encoding,linesep)
	def load(self,filename='',parent_path='',encoding='',func=None,filter_=None):
		if not parent_path:parent_path=self.parent_path
		if filter_:filter_=lambda s:os.path.exists(s) and filter_(s)
		else:filter_=os.path.exists
		if func:func=lambda s:crpath.format(func(s),parent_path)
		else:func=lambda s:crpath.format(s,parent_path)
		super(Paths,self).load(filename,encoding,func=func,filter_=filter_)
	def save(self,filename='',parent_path='',encoding='',linesep='',func=None):
		self.data=list(set(self.data))
		if not linesep:linesep=self.linesep
		if not parent_path:parent_path=self.parent_path
		if not func:super(Paths,self).save(filename,encoding,linesep,func=lambda s:crpath.reformat(s,parent_path))
		else:super(Paths,self).save(filename,encoding,linesep,func=lambda s:func(crpath.reformat(s,parent_path)))