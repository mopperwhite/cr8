#!/usr/bin/python
#encoding=UTF-8

import json
from UserDict import UserDict
class JsonDict(UserDict,object):
	def __init__(self,filename):
		self.filename=filename
		UserDict.__init__(self)
		self.load()
	def load(self):
		self.update(json.load(open(self.filename)))
	def save(self):
		json.dump(dict(self),open(self.filename,'w'))