#!/usr/bin/python
#encoding=UTF-8

class Messager(object):
	def __init__(self,*args,**kwargs):
		self.args=args
		self.kwargs=kwargs
		vars(self).update(kwargs)
	def __iter__(self):
		return iter(self.args)
	def __getitem__(self,key):
		return self.kwargs[key]
	def __repr__(self):
		return "<Messager args=%r kwargs=%r>"%(self.args,self.kwargs)