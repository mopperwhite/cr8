#!/usr/bin/python
#encoding=UTF-8

import cr,os
class CharacterPath(cr.core.Path):
	def __init__(self,ch_pa,parent):
		self.ch_pa=ch_pa
		self.parent=parent
		cr.core.Path.__init__(self,os.path.join(self.ch_pa,'path.ini'),self.ch_pa)
		
