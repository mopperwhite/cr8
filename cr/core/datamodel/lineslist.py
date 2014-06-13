#!/usr/bin/python
#encoding=UTF-8

import re
from UserList import UserList
class LinesList(UserList,object):
	def __init__(self,filename='',encoding='utf-8',linesep='\n'):
		UserList.__init__(self)
		if filename:
			self.linesep=linesep
			self.encoding=encoding
			self.filename=filename
			self.load()
	def load(self,filename='',encoding='',func=None,filter_=None):
		if not encoding:encoding=self.encoding
		if not filename:filename=self.filename
		l=filter(lambda s:s,re.split('[\t\n\r\f\v]',open(filename,'r').read().decode(encoding)))
		if func:l=map(func,l)
		if filter_:l=filter(filter_,l)
		self.extend(l)
	def save(self,filename='',encoding='',linesep='',func=None):
		if not linesep:linesep=self.linesep
		if not encoding:encoding=self.encoding
		if not filename:filename=self.filename
		l=self
		if func:l=map(func,l)
		open(filename,'w').write(linesep.join(l).encode(encoding))