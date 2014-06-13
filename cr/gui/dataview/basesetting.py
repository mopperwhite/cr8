#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from cr.gui import crmessagebox,TextFileEdit,crguiincrease
import cr
class SettingWindowTab(QMainWindow):
	def __init__(self,parent=None):
		QMainWindow.__init__(self,parent)
		self.scroll_area=QScrollArea(self)
		self.setCentralWidget(self.scroll_area)
		self.scroll_area.setWidgetResizable(True)
		Container=QWidget()
		self.scroll_area.setWidget(Container)
		self.Layout=QVBoxLayout(Container)
	def add(self,w):
		self.Layout.addWidget(w)


class BaseSettingWindow(QDialog):
	def __init__(self,setting,parent=None):
		super(BaseSettingWindow,self).__init__(parent)
		self.setting=dict(setting)
		self.__setting=setting
		self.Layout=QVBoxLayout(self)
		self.setWindowTitle(_('setting'))
		
		self.InitButton()
		self.InitTabWidget()
	def InitButton(self):
		self.SaveButton=QPushButton(_('save'))
		self.RestartButton=QPushButton(_('restart to update settings'))
		self.TextButton=QPushButton(_('edit as text'))
		QObject.connect(self.SaveButton, SIGNAL("released()"), self.save)
		QObject.connect(self.RestartButton, SIGNAL("released()"),self.restart)
		QObject.connect(self.TextButton, SIGNAL("released()"), self.edit_as_text)
		widget=QWidget()
		layout=QHBoxLayout(widget)
		layout.addWidget(self.SaveButton)
		layout.addWidget(self.RestartButton)
		layout.addWidget(self.TextButton)
		self.Layout.addWidget(widget)
	def InitTabWidget(self):
		self.TabWidget=QTabWidget()
		self.Layout.addWidget(self.TabWidget)
	def edit_as_text(self):
		def show():
			TextFileEdit(self.__setting.path,parent=self).show()
		crmessagebox.checkedrunning(_('This operation may result in an unknown error.'),show)
	def addTab(self,title):
		tab=SettingWindowTab(self)
		self.TabWidget.addTab(tab,title)
		return tab
	def restart(self):
		crmessagebox.checkedrunning(_('Are you sure?'),CRSignal,'inner.restart')
	def save(self):
		self.__setting.update(self.setting)
		self.__setting.save()