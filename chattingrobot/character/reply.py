#!/usr/bin/python
#encoding=UTF-8

import os,random
import cr
class ReplyBar(cr.core.Database):
	def __init__(self,parent,path):
		super(ReplyBar,self).__init__(path,parent.signal)
		self.edit=cr.gui.DatabaseEdit(self)
		self.edit.setWindowTitle(_('teach')+'-'+parent.name)
	def input(self,s):
		r=self.search(s)
		if r:
			return random.choice(r)
		else:
			return None