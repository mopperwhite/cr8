#!/usr/bin/python
#encoding=UTF-8

import traceback
from cr.core import crtry,Mark
class Target(object):
	def __init__(self,parent,target,*args,**kwargs):
		self.parent=parent
		self.target=target
		self.args=args
		self.kwargs=kwargs
class FuncTarget(Target):
	def __call__(self,*args,**kwargs):
		return self.target(*(self.args+args),**dict(zip(self.kwargs.keys(),self.kwargs.values())+zip(kwargs.keys(),kwargs.values())))
class SignTarget(Target):
	def __call__(self,*args,**kwargs):
		return self.parent.send(self.target,*(self.args+args),**dict(zip(self.kwargs.keys(),self.kwargs.values())+zip(kwargs.keys(),kwargs.values())))
class Slot(object):
	class _Mark(Mark):
		def __init__(self,parent):
			super(Slot._Mark,self).__init__(parent)
		def remove(self):
			self.parent.remove(self)
		def skip(self):
			self.parent.skip=True
	def __init__(self,parent,signal):
		self.parent=parent
		self.signal=signal
		self.skip=False
		self.dic={}
	def add(self,target,*args,**kwargs):
		mark=self._Mark(self)
		if callable(target):
			targ=FuncTarget(self.parent,target,*args,**kwargs)
		else:
			targ=SignTarget(self.parent,target,*args,**kwargs)
		self.dic[mark]=targ
		return mark
	def remove(self,mark):
		del self.dic[mark]
	def __call__(self,*args,**kwargs):
		for t in self.dic.values():
			crtry.run(t,*args,**kwargs)
			if self.skip:
				break
		self.skip=False
	def __iter__(self):
		for i in self.dic.keys():
			yield i
class Caller(object):
	def __init__(self,signal,receive_args,parent):
		self.signal=signal
		self.parent=parent
		self.receive_args=receive_args
	def __call__(self,*args,**kwargs):
		if self.receive_args:
			return self.parent(self.signal,*args,**kwargs)
		else:
			return self.parent(self.signal)
class Signal(object):
	def __init__(self,parent=None):
		self.signal_dic={}
		crtry.checktype('parent',parent,(None,Signal))
		self.parent=parent
	def connectSlot(self,signal):
		self.signal_dic[signal]=Slot(self,signal)
	def updateSlot(self,lis):
		for s in lis:
			self.connectSlot(s)
	def getCaller(self,signal,receive_args=False):
		return Caller(signal,receive_args,self)
	def connect(self,signal,target,*args,**kwargs):
		if not signal:
			raise TypeError("False object cannot be connected as a signal.")
		if isinstance(signal,Slot._Mark):
			raise TypeError("Slot._Mark object cannot be connected as a signal.")
		if signal in self.signal_dic and isinstance(self.signal_dic[signal],Slot):
			return self.signal_dic[signal].add(target,*args,**kwargs)
		else:
			if callable(target):
				self.signal_dic[signal]=FuncTarget(self,target,*args,**kwargs)
			else:
				self.signal_dic[signal]=SignTarget(self,target,*args,**kwargs)
	def remove(self,signal):
		if isinstance(signal,Slot._Mark):
			signal.remove()
		else:
			if signal in self:
				del self.signal_dic[signal]
			else:
				raise Exception('%r is not connected.'%signal)
	def get(self,signal):
		if signal in self.signal_dic:
			return self.signal_dic[signal].target
		elif self.parent:
			return self.parent.get(signal)
		else:raise Exception('%r is not connected.'%signal)		
	def getAllSignals(self):
		if self.parent:
			return self.signal_dic.keys()+self.parent.getAllSignals()
		else:
			return self.signal_dic.keys()
	def send(self,signal,*args,**kwargs):
		if not signal:return
		if signal in self.signal_dic:
			return self.signal_dic[signal](*args,**kwargs)
		elif self.parent:
			return self.parent.send(signal,*args,**kwargs)
		else:raise Exception('%r is not connected.'%signal)
	def safeSend(self,signal,*args,**kwargs):
			return crtry.run(self.send,signal,*args,**kwargs)
	def update(self,dic):
		for s,t in zip(dic.keys(),dic.values()):
			self.connect(s,t)
	def __getitem__(self,signal):
		return self.get(signal)
	def __setitem__(self,signal,target):
		self.connect(signal,target)
	def __delitem__(self,signal):
		self.remove(signal)
	def __call__(self,signal,*args,**kwargs):
		return self.send(signal,*args,**kwargs)
	def __iter__(self):
		for s in self.signal_dic.keys():
			yield s