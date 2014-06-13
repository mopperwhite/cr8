#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
class ErrorMessageBox(QDialog):
	def __init__(self,title='',caption='',inf='',parent=None):
		super(ErrorMessageBox,self).__init__(parent=parent)
		if inf:
			self.inf=inf
		else:
			self.inf=cr.core.crtry.gettraceback()
		if caption:
			self.caption=caption
		else:
			self.caption='Error'
		self.layout=QVBoxLayout(self)
		self.setWindowTitle(_(title))
		self.title_label=QLabel(_(self.caption))
		self.text_browser=QTextBrowser()
		self.text_browser.setReadOnly(True)
		self.text_browser.setText(self.inf)
		self.button_box=QDialogButtonBox(QDialogButtonBox.Ok)
		QObject.connect(self.button_box.button(QDialogButtonBox.Ok), SIGNAL("clicked()"), self, SLOT("close()"))

		self.layout.addWidget(self.title_label)
		self.layout.addWidget(self.text_browser)
		self.layout.addWidget(self.button_box)