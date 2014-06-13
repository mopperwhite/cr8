#!/usr/bin/python
#encoding=UTF-8

from basedatabase import *
from cr.core.control.application import BaseApp,BaseAppBar
from cr.core.datamodel.xmldict import XmlDict
from cr.core.crstr import RegexFormater
from cr.core.crtry import checktype
class DatabaseItem(Unit,BaseApp):
	def onInit(self,dic,path):
		self.path=path
		self.dic=dic
		if not self.readonly:
			self.teach_priority=int(dic['teach_priority'])
		BaseApp.__init__(self,path)
		if 'k' not in dic['order'] or 'v' not in dic['order']:
			raise ValueError('"k" and "v" must be in "order".')
		if 's' in dic['order']:
			self.hassignal=True
			self.call_priority=int(dic['call_priority'])
			self.msger_args_mode=dic['msger_args_mode']
			self.msger_kwarg_name=dic['msger_kwarg_name']
		if 'a' in dic['order']:
			self.hasargs=True
		get_dic=dict([
			('k',lambda s:s.split(dic['sep'])),
			('v',lambda s:s.split(dic['sep'])),
			('s',lambda s:s),
			('a',lambda s:eval(s)),
			])
		format_dic=dict(filter(lambda i:i[0] in dic['order'],
			[('k',lambda e:dic['sep'].join(e.keys())),
			('v',lambda e:dic['sep'].join(e.values())),
			('s',lambda e:e.signal),
			('a',lambda e:repr(e.args)),]))
		init_values={'k':[],'v':[],'s':'','a':()}
		order=dic['order']
		self.formater=RegexFormater(format_=dic['format'],order=dic['order'],init_values=init_values,get_dic=get_dic,format_dic=format_dic,regex_flag=dic['regex_flags'])
	def setFilename(self,f,e):
		self.filename=f
		self.encoding=e
	def loadEntriesFromDict(self,d):
		e=self.getEntry()
		e.updateKeys(d['k'])
		e.updateValues(d['v'])
		e.setSignal(d['s'],d['a'])
		return e
	def load(self,dat):
		self.updateEntries(map(self.loadEntriesFromDict,self.formater.get(dat)))
	def save(self):
		if self.readonly:
			raise Exception('It`s a read-only Unit.')
		if 'teach_priority' in self.dic:
			self.dic['teach_priority']=unicode(self.teach_priority)
		if 'call_priority' in self.dic:
			self.dic['call_priority']=unicode(self.call_priority)
		if 'msger_args_mode' in self.dic:
			self.dic['msger_args_mode']=self.msger_args_mode
		if 'msger_kwarg_name' in self.dic:
			self.dic['msger_kwarg_name']=self.msger_kwarg_name
		self.dic.save()
		open(self.filename,'w').write(self.formater.format(self.entrieslist).encode(self.encoding))







class Database(BaseDatabase,BaseAppBar):
	def __init__(self,path,signal_system=None):
		super(Database,self).__init__(signal_system)
		self.path=path
		self.load()
	def load(self):
		for i in os.listdir(self.path):
			self.load_a_unit(os.path.join(self.path,i))
	def load_a_unit(self,path):
		dic=XmlDict(os.path.join(path,'init.xml'))
		mode_dict={
		'text':self._loadMode_text,
		'text_from_signal':self._loadMode_text_from_signal,
		'signal':self._loadMode_signal,
		}
		if dic['mode'] in mode_dict:
			return mode_dict[dic['mode']](path,dic)
		else:
			raise Exception('%r is an unknown mode.'%dic['mode'])
	def _loadMode_text(self,path,dic):
#		unit=DatabaseItem(parent=self,readonly=eval(dic['readonly']),signal_system=self.signal_system)
		unit=DatabaseItem(readonly=eval(dic['readonly']),signal_system=self.signal_system)
		data=open(os.path.join(path,dic['file'])).read().decode(dic['encoding'])
		unit.setFilename(os.path.join(path,dic['file']),dic['encoding'])
		return self._baseMode_text(data,dic,unit,path)
	def _loadMode_text_from_signal(self,path,dic):
		data=self.signal_system.send(dic['signal'],*eval(dic['args']))
		unit=DatabaseItem(parent=self,readonly=True,signal_system=self.signal_system)
		return self._baseMode_text(data,dic,unit,path)
	def _baseMode_text(self,data,dic,unit,path):
		data=re.sub(dic['note'].decode(dic['encoding']),'',data,flags=RegexFormater.get_flags_from_str(dic['note_regex_flag']))
		unit.onInit(dic,path)
		unit.load(data)
		self.addUnit(unit)
		return unit
	def _loadMode_signal(self,path,dic):
		unit=self.signal_system.send(dic['signal'],Path.DirDict(path),dic)
		checktype('unit',unit,BaseUnit)
		self.addUnit(unit)
		return unit
	def _addValue(self,v):
		super(Database,self)._addValue(v,cmper=lambda e:e.readonly)
	def save(self):
		for u in self.list:
			if not u.readonly:
				u.save() 
	def install(self,filename):
		return self.load_a_unit(super(Database,self).install(filename,self.path))
