#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
class SettingWindowInterface(QObject):
	__setting_window_list=[]
	__setting_window_size=(500,400)
	def __init__(self):
		self.__setting_window_list.append(self)
#		self.resize(*self.__setting_window_size)
	@classmethod
	def setSize(cls,size):
		size=cr.gui.crguiincrease.getsize(size)
		cls.__setting_window_size=size.width(),size.height()
		for widget in cls.__setting_window_list:
			widget.resize(size)
class SettingDialog(QDialog,SettingWindowInterface):
	def __init__(self,parent=None):
		QDialog.__init__(self,parent)
		SettingWindowInterface.__init__(self)
class SettingWidget(QWidget,SettingWindowInterface):
	def __init__(self,parent=None):
		QWidget.__init__(self,parent)
		SettingWindowInterface.__init__(self)
class SettingMainWindow(QMainWindow,SettingWindowInterface):
	def __init__(self,parent=None):
		QMainWindow.__init__(self,parent)
		SettingWindowInterface.__init__(self)