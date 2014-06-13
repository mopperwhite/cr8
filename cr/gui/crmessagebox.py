#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
def warning(value='',parent=None):
	QMessageBox.warning(parent,_('warning'),_(value))
def checkedwarning(value='',parent=None):
	return QMessageBox.warning(parent,_('warning'),_(value),QMessageBox.Yes | QMessageBox.No, QMessageBox.No)==QMessageBox.Yes
def checkedrunning(value,func,*args,**kwargs):
	if checkedwarning(value):
		func(*args,**kwargs)
def information(self,value='',parent=None):
	 QMessageBox.information(parent,_('information'),value)