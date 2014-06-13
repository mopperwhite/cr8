#!/usr/bin/python
#encoding=UTF-8

import types
from UserDict import UserDict
from xml.etree import ElementTree
class XmlDictItem(UserDict,object):
	def DEFAULT_FORMATER(self,st):
		return st
	def __init__(self,element,formater=None,reformater=None):
		if formater:
			self.formater=formater
		else:
			self.formater=self.DEFAULT_FORMATER
		if reformater:
			self.reformater=reformater
		else:
			self.reformater=self.DEFAULT_FORMATER
		self.element=element
		UserDict.__init__(self)
		cl=self.element.getchildren()
		self.update(dict(zip(map(lambda c:c.tag,cl),map(lambda c:XmlDictItem(c,self.formater,self.reformater),cl))))
	def setValue(self,text):
		self.element.text=self.reformater(text)
	def getValue(self):
		return self.formater(self.element.text)
	def getAttrib(self):
		return self.element.attrib
	def setAttrib(self,attrib):
		self.element.attrib=attrib
	def add(self,tag,text='',attrib={}):
		element=ElementTree.SubElement(self.element,tag)
		element.text=self.reformater(text)
		element.attrib=attrib
		UserDict.__setitem__(self,tag,XmlDictItem(element,self.formater,self.reformater))
	def clear(self):
		UserDict.clear(self)
		self.element.clear()
	def __len__(self):
		return len(self.element)
	def __getitem__(self,key):
		i=UserDict.__getitem__(self,key)
		if i:
			return i
		else:
			return i.getValue()
	def __setitem__(self,tag,text):
		if tag in self:
			UserDict.__getitem__(self,tag).setValue(text)
		else:
			self.add(tag,text)
	def __delitem__(self,tag):
		self.element.remove(self[tag].element)
		UserDict.__delitem__(tag)
	def __repr__(self):
		if self:
			return UserDict.__repr__(self)
		else:
			return repr(self.getValue())

class XmlDict(XmlDictItem):
	def __init__(self,filename,formater=None,reformater=None):
		self.tree=ElementTree.parse(filename)
		self.filename=filename
		super(XmlDict,self).__init__(self.tree.getroot(),formater,reformater)
	def save(self):
		self.tree.write(open(self.filename,'w'))