#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr

class ComboBoxDialog(QDialog):
	def __init__(self,title='combo',list_=[],default_value='',use_gettext=True,parent=None):
		super(ComboBoxDialog,self).__init__(parent)
		self.setWindowTitle(_(title))
		self.list_=list(list_)
		self.layout=QVBoxLayout(self)

		self.combobox=QComboBox()
		self.layout.addWidget(self.combobox)
		if use_gettext:
			self.combobox.addItems([_(i) for i in self.list_])
		else:
			self.combobox.addItems(self.list_)
		if default_value in self.list_:
			self.combobox.setCurrentIndex(self.list_.index(default_value))
		self.combobox.setMaxVisibleItems(5)
		
		self.button_box=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		self.layout.addWidget(self.button_box)
		QObject.connect(self.button_box.button(QDialogButtonBox.Cancel), SIGNAL("clicked()"), self, SLOT("close()"))
		QObject.connect(self.button_box.button(QDialogButtonBox.Ok), SIGNAL("clicked()"), self.save)

	def save(self):
		i=self.combobox.findText(self.combobox.currentText())
		self.value=self.list_[i]
		self.close()
	def get(self):
		self.value=self.list_[self.combobox.findText(self.combobox.currentText())]
		self.exec_()
		return self.value