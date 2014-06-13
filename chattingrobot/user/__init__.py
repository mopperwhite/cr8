#!/usr/bin/python
#encoding=UTF-8

import cr,os
class Setting(cr.core.IniSetting):
	def __init__(self,parent):
		self.parent=parent
		super(Setting,self).__init__(self.parent.path['files']['setting'])
class Path(cr.core.Path):
	def __init__(self,parent):
		self.parent=parent
		cr.core.Path.__init__(self,os.path.join(self.parent.dp,'path.ini'),self.parent.dp)
class User:
	def __init__(self,dp):
		self.dp=dp
		self.path=Path(self)
		self.setting=Setting(self)
		self.setting_window=self.getSettingWindow()
		
	def getSettingWindow(self):
		return cr.gui.SettingWindow(self.setting,CRGlobal.init_path['setting_window']['user'])
	def getAppEdit(self):
		return cr.gui.AppManager(self.appbar)

