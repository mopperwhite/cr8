#!/usr/bin/python
#encoding=UTF-8

import cr,os
class CharacterSetting(cr.core.IniSetting):
	def __init__(self,parent):
		self.parnet=parent
		super(CharacterSetting,self).__init__(self.parnet.path['general']['setting'])
