#!/usr/bin/python
#encoding=UTF-8

import re,os,copy
from cr.core import crtry,Messager,NameSpace
DEFAULT_SEARCHER=lambda x,s,flag=re.S|re.I:re.search(x,s,flag) and len(re.search(x,s,flag).group(0))/float(len(s))
DEFAULT_CHECKER=lambda x,s:x==s
ARGS_MODE_FLAGS=NameSpace(
		NO='no',
		BEFORE='before',
		AFTER='after',
		KEYWORD='keyword',
		)
class BaseData(object):
	def __init__(self,parent,value,id,searcher=DEFAULT_SEARCHER,attrib={}):
		self.parent=parent
		self.value=value
		self.searcher=searcher
		self.id=id
		self.attrib=attrib
	def compare(self,st):
		return self.searcher(self.value,st)
	def __getitem__(self,ke):
		return self.attrib[ke]
	def __hash__(self):
		return hash(self.value)
	def __eq__(self,other):
		if not isinstance(other,BaseData):return False
		return self.value==other.value
	def __repr__(self):
		return "<%s instance at %#x value=%r parent=%s>"%(self.__class__.__name__,id(self),self.value,self.parent)
class Key(BaseData):pass
class Value(BaseData):pass

#EEEEE  N   N  TTTTT  RRRR   Y   Y
#E      N   N    T    R   R  Y   Y
#E      NN  N    T    R   R   Y Y
#EEEE   N N N    T    RRRR     Y
#E      N  NN    T    R R      Y
#E      N   N    T    R  R     Y
#EEEEE  N   N    T    R   R    Y


class Entry(object):
	EntryDict={}
	def __init__(self,readonly=True,attrib={},searcher=DEFAULT_SEARCHER,signal_system=None):
		if signal_system:
			self.signal_system=signal_system
		else:
			self.signal_system=CRSignal
		self.readonly=readonly
		self.attrib=attrib
		self.searcher=searcher
		self.id=self._getID()
		self.EntryDict[self.id]=self
		self.keyslist=[]
		self.valueslist=[]
		self.signal=''
		self.args=()
	def setId(self,id):
		self.id=id
		for i in self.keyslist+self.valueslist:
			i.id=id
	def getId(self):
		return self.id
	def getAttrib(self):
		return self.attrib.copy()
	def setAttrib(self,**attrib):
		self.attrib=attrib
		for i in self.keyslist+self.valueslist:
			i.attrib=self.attrib
	def setSignal(self,signal,args=()):
		self.signal=signal
		self.args=args
	def keys(self):
		return map(lambda i:i.value,self.keyslist)
	def getKey(self,k):
		return Key(self,k,self.id,self.searcher,self.attrib)
	def addKey(self,k):
		if k not in self:
			key=self.getKey(k)
			self.keyslist.append(key)
			return key
	def updateKeys(self,l):
		for i in l:
			self.addKey(i)
	def removeKey(self,k):
		if k in self:
			self.keyslist.remove(self.getKey(k))
	def checkKey(self,k,checker=DEFAULT_CHECKER):
		return bool(filter(lambda k_:checker(k,k_),self))
	def values(self):
		return map(lambda i:i.value,self.valueslist)
	def getValue(self,v):
		return Value(self,v,self.id,self.searcher)
	def addValue(self,v):
		if v not in map(lambda x:x.value,self.valueslist):
			value=self.getValue(v)
			self.valueslist.append(value)
			return value
	def updateValues(self,l):
		for v in l:
			self.addValue(v)
	def removeValue(self,v):
		if v in self.values():
			self.valueslist.remove(self.getValue(v))
			return True
	def checkValue(self,v,checker=DEFAULT_CHECKER):
		if not self:return 0
		return bool(filter(lambda k_:checker(k,k_.value),self.valueslist))
	@classmethod
	def _getID(cls):
		cls.__idnumber=0
		while True:
			yield 'entry-'+hex(cls.__idnumber)
			cls.__idnumber+=1
	def __len__(self):
		return len(self.keyslist)
	def __iter__(self):
		for i in self.keys():
			yield i
	def __call__(self,msger,mode=ARGS_MODE_FLAGS.NO,msger_kwarg_name='messager'):
		if mode==ARGS_MODE_FLAGS.NO:
			self.signal_system.safeSend(self.signal,*self.args)
		elif mode==ARGS_MODE_FLAGS.BEFORE:
			self.signal_system.safeSend(self.signal,msger,*self.args)
		elif mode==ARGS_MODE_FLAGS.AFTER:
			self.signal_system.safeSend(self.signal,*self.args+(msger,))
		elif mode==ARGS_MODE_FLAGS.KEYWORD:
			self.signal_system.safeSend(self.signal,*self.args,**{msger_kwarg_name:msger})
		else:
			raise ValueError('Unknown mode %r.'%mode)
	def __add__(self,other):
		me_=max(self,other,key=lambda e:not e.readonly)
		if me_==self:
			oe=other
		else:
			oe=self
		me=copy.copy(me_)
		me.keyslist=[]
		me.valueslist=[]
		me.updateKeys(set(map(lambda k:k.value,me_.keyslist+oe.keyslist)))
		me.updateValues(set(map(lambda v:v.value,me_.valueslist+oe.valueslist)))
		return me
	def __getitem__(self,k):
		return self.attrib.__getitem__(k)







class BaseUnit(object):
	msger_kwarg_name='messager'
	msger_args_mode=ARGS_MODE_FLAGS.NO
	call_priority=0
	teach_priority=0
	hassignal=False
	hasargs=False
	def __raiseException(self,func):
		raise Exception('%r is not covered.'%func.func_name)
	def keys(self):
		self.__raiseException(self.keys)
	def values(self):
		self.__raiseException(self.values)
	def addKey(self,k1,k2,checker=DEFAULT_CHECKER):
		self.__raiseException(self.addKey)
	def addValue(self,k,v,checker=DEFAULT_CHECKER):
		self.__raiseException(self.addValue)
	def removeKey(self,k):
		self.__raiseException(self.removeKey)
	def removeValue(self,v):
		self.__raiseException(self.removeValue)
	def search(self,s):
		self.__raiseException(self.search)
	def randomValue(self,k):
		self.__raiseException(self.randomValue)
	def call(self,k,*args,**kwargs):
		pass
	@classmethod
	def _getID(cls):
		cls.__idnumber=0
		while True:
			yield 'unit-'+hex(cls.__idnumber)
			cls.__idnumber+=1
#U   U  N   N  IIIII  TTTTT
#U   U  N   N    I      T
#U   U  NN  N    I      T
#U   U  N N N    I      T
#U   U  N  NN    I      T
#U   U  N   N    I      T
# UUU   N   N  IIIII    T

class Unit(BaseUnit):
	def __init__(self,readonly=True,signal_system=None):
		if signal_system:
			self.signal_system=signal_system
		else:
			self.signal_system=CRSignal
		self.id=self._getID()
		self.readonly=readonly
		self.entrieslist=[]
	def getEntry(self):
		return Entry(readonly=self.readonly,signal_system=self.signal_system)
	def entries(self):
		return list(self.entrieslist)
	def addEntry(self,entry):
		crtry.checktype('entry',entry,Entry)
		self.entrieslist.append(entry)
	def getNotReadOnlyEntries(self):
		return filter(lambda e:not e.readonly,self.entrieslist)
	def updateEntries(self,l):
		for i in l:
			self.addEntry(i)
	def removeEntry(self,entry):
		if entry in self.entrieslist:
			self.entrieslist.remove(entry)
			return True

	def getKeys(self):
		return reduce(lambda l,e:l+e.keyslist,[[]]+self.entrieslist)
	def getValues(self):
		return reduce(lambda l,e:l+e.valueslist,[[]]+self.entrieslist)
	def keys(self):
		return reduce(lambda l,e:l+e.keys(),[[]]+self.entrieslist)
	def values(self):
		return reduce(lambda l,e:l+e.values(),[[]]+self.entrieslist)
	def _edit(self,s,key_func,func,func_2):
		el=self.getNotReadOnlyEntries()
		for e in el:
			if key_func(e):
				func(s,e)
				return True
		func_2()
		return None
	def _edit_byKey(self,s1,s2,func,func_2,checker=DEFAULT_CHECKER):
		return self._edit(s2,lambda x:x.checkKey(s1,checker),func,func_2)
	def _edit_byValue(self,s1,s2,func,func_2,checker=DEFAULT_CHECKER):
		return self._edit(s2,lambda x:x.checkValue(s1,checker),func,func_2)
	def addKey(self,k1,k2,checker=DEFAULT_CHECKER):
		l=[(DEFAULT_CHECKER(k1,k.value),k) for k in self.getKeys()]
		if l:
			mxP,mxK=max(l,key=lambda x:x[0])
			if mxP==1:
				return mxK.parent.addKey(k2)
	def addValue(self,k,v,checker=DEFAULT_CHECKER):
		l=[(DEFAULT_CHECKER(k,ki.value),ki) for ki in self.getKeys()]
		if l:
			mxP,mxV=max(l,key=lambda x:x[0])
			if mxP==1:
				return mxV.parent.addValue(v)
	def removeKey(self,k):
		return reduce(lambda x,y:x or y.removeKey(k),[False]+self.entrieslist)
	def removeValue(self,v):
		return reduce(lambda x,y:x or y.removeValue(v),[False]+self.entrieslist)

	def call(self,k,s):
		msger=Messager(	
						string=s,
						key=k,
						unit=self,
						)
		for e in self.entrieslist:
			if k in e or k in e.keyslist:
				return e(msger,self.msger_args_mode,self.msger_kwarg_name)
	def search(self,s):
		if not self.getKeys():
			return None
		l=[(k.compare(s),k) for k in self.getKeys()]
		mxP,mxK=max(l,key=lambda i:i[0])
		mxVs=reduce(lambda x,y:x+y,[[],[]]+[k.parent.values() for p,k in l if p==mxP])
		if not mxP:
			return None
		else:
			return Messager(key=mxK,score=mxP,values=mxVs,parent=self)



#DDD      A    TTTTT    A    BBBB     A     SSS   EEEEE
#D  D     A      T      A    B   B    A    S   S  E
#D   D   A A     T     A A   B   B   A A   S      E
#D   D   A A     T     A A   BBBB    A A    SSS   EEEE
#D   D  AAAAA    T    AAAAA  B   B  AAAAA      S  E
#D  D   A   A    T    A   A  B   B  A   A  S   S  E
#DDD    A   A    T    A   A  BBBB   A   A   SSS   EEEEE



class BaseDatabase(object):
	def __init__(self,signal_system=None):
		if signal_system: self.signal_system=signal_system
		else: self.signal_system=CRSignal
		self.list=[]
	def getUnit(self,readonly=True):
		return Entry(readonly,signal_system=self.signal_system)
	def addUnit(self,unit):
		crtry.checktype('unit',unit,Unit)
		self.list.append(unit)
	def getEntry(self,ignore=False):
		ul=self.notReadonlyUnits()
		if ul:
			entry=ul[0].getEntry()
			ul[0].addEntry(entry)
			return entry
		elif not ignore:
			raise Exception("All the units are readonly.") 
	def removeEntry(self,entry):
		return reduce(lambda b,u:b or u.removeEntry(entry),self.list)
	def _unitsOperate(self,no_readonly,func):
		if no_readonly:l=self.list
		else:l=self.notReadonlyUnits()
		if l:return reduce(lambda x,y:x or func(y),[False]+l)
		else:return None
	def addKey(self,k1,k2,no_readonly=True,checker=DEFAULT_CHECKER):
		if not self._unitsOperate(no_readonly,lambda u:u.addKey(k1,k2,checker)):
			l=self.notReadonlyUnits()
			if l:
				unit=max(l,key=lambda u:u.teach_priority)
				entry=unit.getEntry()
				entry.addKey(k1)
				entry.addKey(k2)
				unit.addEntry(entry)
				return True
		return False
	def addValue(self,k,v,no_readonly=True,checker=DEFAULT_CHECKER):
		if not self._unitsOperate(no_readonly,lambda u:u.addValue(k,v,checker)):
			l=self.notReadonlyUnits()
			if l:
				unit=max(l,key=lambda u:u.teach_priority)
				entry=unit.getEntry()
				entry.addKey(k)
				entry.addValue(v)
				unit.addEntry(entry)
				return True
		return False
	def removeKey(self,k,no_readonly=True):
		return self._unitsOperate(no_readonly,lambda u:u.removeKey(k))
	def removeValue(self,v,no_readonly=True):
		return self._unitsOperate(no_readonly,lambda u:u.removeValue(v))
	def units(self):
		return list(self.list)
	def notReadonlyUnits(self):
		return [u for u in self.list if not u.readonly]
	def entries(self):
		return reduce(lambda l,u:l+u.entrieslist,[[]]+self.list)
	def notReadonlyEntries(self):
		return reduce(lambda l,u:l+u.entrieslist,[[]]+self.notReadonlyUnits())
	def search(self,s):
		ml=filter(lambda m:bool(m),map(lambda u:u.search(s),self.list))
		if ml:
			mxM=max(ml,key=lambda m:m.score)
			l=[m for m in ml if m.score==mxM.score]
			values=reduce(lambda x,y:x+y,[[],[]]+map(lambda m:m.values,l))
			mxSU=max(map(lambda m:m.parent,l),key=lambda u:u.call_priority*u.hassignal)
			mxSU.call(mxM.key,s)
			return values
		else:	return None