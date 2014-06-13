#!/usr/bin/python
#encoding=UTF-8

from cr.core.datamodel.dirdict import DirDict
from cr.core import crstr,crtry
from UserDict import UserDict
DEFAULT_FORMATER=crstr.RegexFormater(format_='[MsgID=%s||MsgStr=%s]',order=('msgid','msgstr'),regex_flag='SI')
class GetText(UserDict,object):
	def __init__(self,parent=None):
		crtry.checktype('parent',parent,(None,GetText))
		self.parent=parent
		self.kwargs_mark="%s"
		self.childrenlist=[]
		self.dir=None
		self.lang=None
		self.record=set([])
		UserDict.__init__(self)
	def load(self,dirpath,lang='',formater=DEFAULT_FORMATER,encoding='utf-8'):
		crtry.checktype('formater',formater,crstr.RegexFormater)
		self.dirpath=dirpath
		self.dir=DirDict(dirpath)
		self.setLanguage(lang)
		self.formater=formater
		self.encoding=encoding
		self.update(dict(map(lambda i:(i['msgid'],i['msgstr']),self.formater.get(open(self.dir[self.lang]).read().decode(self.encoding)))))
	def setLanguage(self,lang):
		if lang:
			self.lang=lang
		elif self.parent:	
			self.lang=self.parent.lang
		else:
			raise Exception('At least one of "lang" and "parent" should be set.')
		if lang not in self.dir and lang!=parent.lang:
			raise Exception('Language %r does not exist.'%lang)
	def save(self,ignore=False):
		if self.dir:
			s=self.formater.format(map(lambda i:{'msgid':i[0],'msgstr':i[1]},zip(self.keys(),self.values())))
			self.dir[self.lang]=s.encode(self.encoding)
			return True
		elif ignore:
			return False
		else:
			raise Exception('Cannot save GetText , "load" was never called.')
	def fortstr(self,s,args=(),kwargs={}):
		if kwargs:
			s=reduce(lambda x,y:x.replace(y,self.kwargs_mark%kwargs[y]),[s]+kwargs.keys())
		try:s=s%args
		except:pass
		return s
	def get(self,id):
		return self[id]
	def add(self,id,str_):
		self[id]=str_
	def remove(self,id):
		del self[id]
	def update(self,target):
		if isinstance(target,GetText):
			self.childrenlist.insert(0,target)
		else:
			UserDict.update(self,target)
	def format(self,id,*args,**kwargs):
		chi=filter(lambda c:id in c,self.childrenlist)
		self.record.add(id)
		if chi:
			return chi[0].format(id,*args,**kwargs)
		elif id in self:
			return self.fortstr(self[id],args,kwargs)
		elif self.parent:
			return self.parent.format(id,*args,**kwargs)
		else:
			return self.fortstr(id,args,kwargs)
	def getRecord(self):
		return list(self.record)
	def __call__(self,id,*args,**kwargs):
		return self.format(id,*args,**kwargs)
	def __iter__(self):
		return iter(self.keys())