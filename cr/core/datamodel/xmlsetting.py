#!/usr/bin/python
#encoding=UTF-8

from xmldict import XmlDict
class XmlSetting(XmlDict):
	def __init__(self,filename,formater=None,reformater=None):
		if formater:
			formater_=lambda s:eval(formater(s))
		else:
			formater_=eval
		if reformater:
			reformater_=lambda s:reformater(repr(s))
		else:
			reformater_=repr
		super(XmlSetting,self).__init__(filename,formater_,reformater_)