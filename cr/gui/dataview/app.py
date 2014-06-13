#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from cr.gui import crmessagebox
import cr
class AppManager(QDialog):
	def __init__(self,appbar,parent=None):
		self.appbar=appbar
		super(AppManager,self).__init__(parent)
		
		self.setWindowTitle(_('App Manager'))

		self.layout=QVBoxLayout(self)
		self.button_layout=QHBoxLayout()

		self.install_button=QPushButton(_('install'))
		self.pack_button=QPushButton(_('pack'))
		self.uninstall_button=QPushButton(_('uninstall'))
		self.restart_button=QPushButton(_('restart to update settings'))

		QObject.connect(self.install_button,SIGNAL("released()"),self.install)
		QObject.connect(self.pack_button,SIGNAL("released()"),self.pack)
		QObject.connect(self.uninstall_button,SIGNAL("released()"),self.uninstall)
		QObject.connect(self.restart_button, SIGNAL("released()"),self.restart)

		self.list_widget=QListWidget()

		self.button_layout.addWidget(self.install_button)
		self.button_layout.addWidget(self.pack_button)
		self.button_layout.addWidget(self.uninstall_button)
		self.layout.addLayout(self.button_layout)
		self.layout.addWidget(self.restart_button)
		
		self.layout.addWidget(self.list_widget)


		self.file_dialog=QFileDialog()

		for a in self.appbar.list:
			self.list_widget.addItem(a.id)
	def getChosenItem(self,rmitem=False):
		l=self.list_widget.selectedItems()
		if not l:
			return
		sel=l[0]
		if sel:
			s=unicode(sel.text())
			if rmitem:
				self.list_widget.takeItem(self.list_widget.row(sel))
			return filter(lambda a:a.id==s,self.appbar.list)[0]
	def install(self):
		p=unicode(self.file_dialog.getOpenFileName(self))
		if p:
			app=self.appbar.install(p)
			if isinstance(app,cr.core.Application):
				self.list_widget.addItem(app.id)
			else:
				self.list_widget.addItem(unicode(app))
	def pack(self):
		a=self.getChosenItem(False)
		p=unicode(self.file_dialog.getSaveFileName(self))
		if a and p:
			a.pack(p)
	def uninstall(self):
		a=self.getChosenItem(True)
		a.uninstall()
	def restart(self):
		crmessagebox.checkedrunning(_('Are you sure?'),CRSignal,'inner.restart')