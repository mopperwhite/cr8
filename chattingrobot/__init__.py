#!/usr/bin/python
#encoding=UTF-8

import os,traceback,shutil

from PyQt4.QtGui import *

import cr
from user import User
from user._character import CharacterBar
from user.about import AboutWindow
from character import Character
class ChattingRobotApp(cr.CRMainApplication):
	VERSION="CR 8.01"
	def __init__(self,initfile):
		super(ChattingRobotApp,self).__init__()
		self.initGlobalPath(initfile)
		self.initSelf()
		self.initSlots()
		self.initUser()
		self.initGlobal()
		self.initApps()
		self.initCharacters()
		self.initSettingWindows()
		self.initSignals()

	def initGlobalPath(self,initfile):
		CRGlobal.init_path=cr.core.Path(initfile)


	def initGlobal(self):
		CRGlobal.qss=CRGlobal.init_path['local']['style_sheet']
		self.warn_when_quit=self.user.setting['global']['warn_when_quit']
		CRGlobal.gettext.load(CRGlobal.init_path['local']['gettext'],self.user.setting['global']['language'])
#		cr.gui.SettingWindowInterface.setSize(self.user.setting['global']['setting_window_size'])

	def initSelf(self):
		self.setWindowIcon(QIcon(CRGlobal.init_path['local']['icon']))
		self.setStyleSheet(open(CRGlobal.init_path['local']['style_sheet']).read())

	def initApps(self):
		self.user.appbar=cr.core.AppBar(self.user.path['directories']['apps'])
		self.user.appedit=self.user.getAppEdit()


	def initUser(self):
		self.user=User(CRGlobal.init_path['users']['user'])

	def initSettingWindows(self):
		self.gettext_manager=cr.gui.GetTextManager()
		self.aboutwindow=AboutWindow()

		self.all_character_setting_window=QTabWidget(None)
		self.all_character_setting_window.resize(*CRGlobal.setting_window_size)
		self.all_character_setting_window.setWindowTitle(_('Character Setting'))
		for c in self.characterbar:
			self.all_character_setting_window.addTab(c.getSettingWindow(),u"%s(%s)"%(c.name,c.id))
		
		all_character_setting_window=QTabWidget(None)
		all_character_setting_window.resize(*CRGlobal.setting_window_size)
		for c in self.characterbar:
			all_character_setting_window.addTab(c.getSettingWindow(),u"%s(%s)"%(c.name,c.id))
		
		user_setting_window=self.user.getSettingWindow()

		self.all_setting_window=QTabWidget(None)
		self.all_setting_window.resize(*CRGlobal.setting_window_size)
		self.all_setting_window.setWindowTitle(_('Setting'))
		self.all_setting_window.addTab(user_setting_window,_('user'))
		self.all_setting_window.addTab(all_character_setting_window,_('characters'))


		self.appedit=self.user.getAppEdit()
		self.characteredit=cr.gui.AppManager(self.characterbar)
		self.characteredit.setWindowTitle(_('Character Manager'))

		self.character_app_edit=QTabWidget(None)
		self.character_app_edit.resize(*CRGlobal.setting_window_size)
		self.character_app_edit.setWindowTitle(_('Character App Manager'))
		for c in self.characterbar:
			self.character_app_edit.addTab(c.getAppEdit(),u"%s(%s)"%(c.name,c.id))

	def initCharacters(self):
		self.characterbar=CharacterBar(self.user)

	def installCharacter(self,filename):
		try:
			dir_=os.path.join(self.user.characterspaths.parent_path,os.path.splitext(os.path.split(filename)[1])[0])
			if not os.path.exists(dir_):
				os.mkdir(dir_)
			else:
				shutil.rmtree(dir_)
			cr.core.crzip.unpack(filename,dir_)
		except:
			traceback.print_exc()
			return None

	def initSlots(self):
		l=[
		'inner.reply',
		]
		CRSignal.updateSlot(l)

	def initSignals(self):
		l=[
		('inner.installApp',self.user.appbar.install),
		('inner.installCharacter',self.characterbar.install),
		('inner.showAppManager',self.appedit.show),
		('inner.showCharacterManager',self.characteredit.show),
		('inner.showCharacterAppManager',self.character_app_edit.show),
		('inner.showUserSetting',self.user.setting_window.show),
		('inner.showCharactersSetting',self.all_character_setting_window.show),
		('inner.showGetTextManager',self.gettext_manager.show),
		('inner.showSetting',self.all_setting_window.show),
		('inner.reply',self.reply),
		('inner.showAbout',self.aboutwindow.show),
		('inner.stop',self.stop),
		('inner.clear',self.clear),
		]
		CRSignal.update(dict(l))

	def reply(self,s):
		for i in self.characterbar:
			i.reply(s)	
	def stop(self):
		for i in self.characterbar:
			i.stop()
	def clear(self):
		for i in self.characterbar:
			i.clear()