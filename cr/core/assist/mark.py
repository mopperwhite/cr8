#!/usr/bin/python
#encoding=UTF-8

class Mark(object):
	__mark_number=0
	def __init__(self,parent=None):
		self.parent=parent
		self.id=self.__count()
	@classmethod
	def __count(cls):
		cls.__mark_number+=1
		return cls.__mark_number-1
	def __repr__(self):
		return "<Mark id=%s hash=%s at %s>"%(hex(self.id),hash(self),id(self))