#!/usr/bin/python
#encoding=UTF-8

from inidict import IniDict
class IniSetting(IniDict):
	def __init__(self,filename):
		super(IniSetting,self).__init__(filename)
		self.addGetFormater(eval)
		self.addSetFormater(repr)