#!/usr/bin/python
#encoding=UTF-8

import os,sys

from PyQt4 import QtGui 

import gui
import core

class CRMainApplication(QtGui.QApplication):
	warn_when_quit=True
	def __init__(self):
		QtGui.QApplication.__init__(self,sys.argv)
		self.__initCR()
		self.__initSlots()
		self.__initSignals()
		self.setQuitOnLastWindowClosed(False)
	def __initCR(self):
		import init
		self.__crGlobal=init.Global()
	def addModuleDir(self,dir):
		sys.path.append(dir)
	def __initSlots(self):
		l=[
		'inner.output',
		'inner.restart',
		'inner.showMainWindow',
		]
		CRSignal.updateSlot(l)
	def __initSignals(self):
		sl=[
		('inner.quit',self.Exit),
		('inner.app.SystemTrayIcon',lambda :self.SystemTrayIcon),
		('inner.restart',self.restart),
		]
		CRSignal.update(dict(sl))
	def restart(self):
		os.execl(sys.executable,sys.executable,*sys.argv)
	def Exit(self):
		if self.warn_when_quit:
			gui.crmessagebox.FuncCheckWarning('Are you sure?',self.exit)
		else:
			self.exit()
__all__=['gui','core','CRMainApplication']