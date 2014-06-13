#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from cr.gui import crmessagebox
import cr
class CoupleDialog(QDialog):
	def __init__(self,title='get couple',key_title='key',value_title='value',parent=None):
		super(CoupleDialog,self).__init__(parent)
		self.setWindowTitle(_(title))

		self.layout=QVBoxLayout(self)

		self.key_title=key_title
		self.value_title=value_title

		self.key_layout=QHBoxLayout()
		self.key_label=QLabel(_(key_title))
		self.key_edit=QLineEdit()
		self.key_layout.addWidget(self.key_label)
		self.key_layout.addWidget(self.key_edit)
		self.layout.addLayout(self.key_layout)

		self.value_layout=QHBoxLayout()
		self.value_label=QLabel(_(value_title))
		self.value_edit=QLineEdit()
		self.value_layout.addWidget(self.value_label)
		self.value_layout.addWidget(self.value_edit)
		self.layout.addLayout(self.value_layout)

		
		self.buttons_layout=QHBoxLayout()
		self.ok_button=QPushButton(_('ok'))
		self.cancel_button=QPushButton(_('cancel'))
		self.buttons_layout.addWidget(self.ok_button)
		self.buttons_layout.addWidget(self.cancel_button)
		self.layout.addLayout(self.buttons_layout)
		QObject.connect(self.ok_button,SIGNAL("released()"),self.ok)
		QObject.connect(self.cancel_button,SIGNAL("released()"),self.close)
	def ok(self):
		if self.key_edit.text() and self.value_edit.text():
			key=unicode(self.key_edit.text())
			value=unicode(self.value_edit.text())
			self.result=cr.core.Messager(key,value,key=key,value=value)
			self.close()
		else:
			crmessagebox.warning(_('The "%s" and "%s" cannot be empty.',_(self.key_title),_(self.value_title)))
	def get(self):
		self.key_edit.clear()
		self.value_edit.clear()
		self.result=None
		self.exec_()
		return self.result