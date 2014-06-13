#!/usr/bin/python
#encoding=UTF-8

class NameSpace(object):
	def __init__(self,**kwargs):
		self.__kwargs=kwargs
		vars(self).update(kwargs)
	def values(self):
		return self.__kwargs.values()
	def __getitem__(self,key):
		return self.__kwargs[key]
	def __iter__(self):
		return self.__kwargs.iterkeys()