#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
from errormessagebox import ErrorMessageBox
class LineEditDialog(QDialog):
	def __init__(self,title='value',default_value='',parent=None):
		super(LineEditDialog,self).__init__(parent)
		self.setWindowTitle(_(title))
		self.layout=QVBoxLayout(self)

		self.lineedit=QLineEdit()
		self.lineedit.setText(default_value)
		self.layout.addWidget(self.lineedit)
		self.button_box=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		self.layout.addWidget(self.button_box)
		QObject.connect(self.button_box.button(QDialogButtonBox.Cancel), SIGNAL("clicked()"), self, SLOT("close()"))
		QObject.connect(self.button_box.button(QDialogButtonBox.Ok), SIGNAL("clicked()"), self.save)

		self.func=None
	def setFormater(self,func):
		self.func=func
	def save(self):
		if self.func:
			try:
				string=unicode(self.lineedit.text())
				self.value=self.func(string)
				self.close()
			except:
				emb=ErrorMessageBox('value error',cr.core.crtry.gettraceback(),self)
				emb.exec_()
		else:
			self.value=unicode(self.lineedit.text())
			self.close()
	def get(self):
		self.value=u''
		self.exec_()
		return self.value