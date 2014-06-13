#!/usr/bin/python
#encoding=UTF-8

import os
from cr.core import BaseAppBar
from chattingrobot.character import Character
class CharacterBar(BaseAppBar):
	def __init__(self,parent):
		self.parent=parent
		super(CharacterBar,self).__init__(Character)
		for p in os.listdir(self.parent.path['directories']['characters']):
			self.load(os.path.join(self.parent.path['directories']['characters'],p),self.parent)
	def install(self,filename):
		return super(CharacterBar,self).install(filename,self.parent.path['directories']['characters'])