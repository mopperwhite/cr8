#!/usr/bin/python
#encoding=UTF-8

import os,types

from cr.core.crtry import checktype

class DirDict(object):
	def __init__(self,path):
		self.path=path
	def keys(self):
		return os.listdir(self.path)
	def values(self):
		return [os.path.join(self.path,i) for i in os.listdir(self.path)]
	def iterkeys(self):
		return iter(os.listdir(self.path))
	def itervalues(self):
		return (os.path.join(self.path,i) for i in os.listdir(self.path))
	def items(self):
		return [(i,os.path.join(self.path,i)) for i in os.listdir(self.path)]
	def iteritems(self):
		return ((i,os.path.join(self.path,i)) for i in os.listdir(self.path))
	def __iter__(self):
		for i in os.listdir(self.path):
			if os.path.isfile(os.path.join(self.path,i)):
				yield os.path.splitext(i)[0]
		for i in os.listdir(self.path):
			yield i
	def __getitem__(self,key):
		if key not in self:
			raise KeyError(key)
		if os.path.isdir(key):
			return DirDict(os.path.join(self.path,key))
		else:
			if key in os.listdir(self.path):
				return os.path.join(self.path,key)
			else:
				for i in os.listdir(self.path):
					if key==os.path.splitext(i)[0]:
						return os.path.join(self.path,i)
	def __delitem__(self,key):
		if os.path.isfile(os.path.join(self.path,key)):
			os.remove(os.remove(os.path.join(self.path,key)))
		else:
			shutil.rmtree(os.path.join(self.path,key))
	def __setitem__(self,key,value):
		fp=os.path.join(self.path,key)
		if isinstance(value,types.StringTypes):
			open(fp,'w').write(value)
		elif isinstance(value,DirDict):
			shutil.copytree(value.path,fp)
		else:
			open(fp,'w').write(value.read())