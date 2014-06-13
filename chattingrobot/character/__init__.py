#!/usr/bin/python
#encoding=UTF-8

import os,shutil

from PyQt4.QtCore import *

import cr
from path import CharacterPath
from setting import CharacterSetting
from reply import ReplyBar
from outputbox import OutputBar,OutputBox
from characterwindow import CharacterWindow

class Character(cr.core.BaseApp):
	character_list=[]
	def __init__(self,dp,parent=None):
		self.parent=parent
		self.path=CharacterPath(dp,self)
		self.id=os.path.basename(dp)
		self.path_edit=self.getPathEdit()

		self.setting=CharacterSetting(self)
		self.name=self.setting['general']['name']
		self.outputbar=OutputBar(self)
		self.setting_window=self.getSettingWindow()
		self.signal=cr.core.Signal(CRSignal)
		self.replybar=ReplyBar(self,self.path['general']['reply'])
		self.reply_settingwindow=self.replybar.edit
		self.window=CharacterWindow(self)
		self.initSlots()
		self.initSignals()
		self.initApps()
		self.echo_timer_list=[]
		self.character_list.append(self)
		super(Character,self).__init__(dp,self.id)
		self.signal.send('character.init')
	def initApps(self):
		self.appbar=cr.core.AppBar(self.path['app']['app'],
						globals={
							"CRSignal":self.signal,
							"CharacterSetting":self.setting})
		self.appedit=self.getAppEdit()
		self.signal.update(dict([
		('character.installApp',self.appbar.install),
		('character.showAppManager',self.appedit.show),]))
	def initSignals(self):
		l=[('character.hide',self.window.hide),
		('character.show',self.window.show),
		('character.setMask',self.window.setMask),
		('character.setBackground',self.window.setBackground),
		('character.teach',self.reply_settingwindow.show),
		('character.stop',self.stop),
		('character.clear',self.clear),
		('character.addLoopAction',self.window.addLoopAction),
		('character.addSignalAction',self.window.addSignalAction),
		]
		self.signal.update(dict(l))
	def initSlots(self):
		l=[
		'character.clicked',
		'character.double_clicked',
		'character.outputbox.clicked',
		'character.outputbox.double_clicked',
		'character.say',
		'character.say_with_string',
		'character.input',
		'character.init',
		]
		self.signal.updateSlot(l)
	def output(self,s,wait=True):
		self.signal.send('character.say')
		self.signal.send('character.say_with_string',s)
		self.outputbar.output(s)
	def send_echo(self,s):
		for i in filter(lambda x:x!=self,self.character_list):
			timer=QTimer()
			self.echo_timer_list.append(timer)
			def _echo():
				i.echo(cr.core.Messager(string=s,parent=self))
				timer.stop()
				self.echo_timer_list.remove(timer)
			QObject.connect(timer,SIGNAL("timeout()"),_echo)
			timer.start(self.setting['general']['wait_time'])
	def echo(self,messager):
		if messager.string:
			s=self.get_reply(messager.string)
			if s:
				self.output(self.reply_character_format(cr.core.crstr.replace_html_linesep(self.setting['general']['reply_character_format']%s),messager.parent))
				self.send_echo(s)
	def get_reply(self,s):
		return self.replybar.input(s)
	def reply(self,s):
		self.signal.send('character.input')
		if s:
			r=self.get_reply(self.user_input_format(cr.core.crstr.replace_html_linesep(self.setting['general']['reply_user_format']%s)))
			if r:
				self.output(self.user_output_format(r),False)
				if self.parent.setting['character']['echo'] and self.setting['general']['echo']:
					self.send_echo(r)
			elif self.parent.setting['character']['teachable'] and self.setting['general']['teachable']:
				self.reply_settingwindow.show(s)
	def user_input_format(self,s):
		dic={'@USERNAME':self.parent.setting['general']['name'],
		 '@CHARACTERNAME':self.setting['general']['name'],
		 }
		return reduce(lambda x,y:x.replace(y[1],y[0]),[s]+zip(dic.keys(),dic.values()))
	def user_output_format(self,s):
		dic={'@USERNAME':self.parent.setting['general']['name'],
		 '@CHARACTERNAME':self.setting['general']['name'],
		 }
		return reduce(lambda x,y:x.replace(y[0],y[1]),[s]+zip(dic.keys(),dic.values()))
	def reply_character_format(self,s,other):
		dic={'@USERNAME':other.setting['general']['name'],
		 '@CHARACTERNAME':self.setting['general']['name'],
		 }
		return reduce(lambda x,y:x.replace(y[0],y[1]),[s]+zip(dic.keys(),dic.values()))
	def __repr__(self):
		return '<Character id=%s>'%self.id
	def getSettingWindow(self):
		return cr.gui.SettingWindow(self.setting,CRGlobal.init_path['setting_window']['character'])
	def getAppEdit(self):
		appedit=cr.gui.AppManager(self.appbar)
		appedit.setWindowTitle(_('Character App Manager'))
		return appedit
	def getPathEdit(self):
		return cr.gui.PathEdit(self.path)
	def stop(self):
		for timer in self.echo_timer_list:
			timer.stop()
		self.echo_timer_list=[]
	def clear(self):
		self.outputbar.stop()