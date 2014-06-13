#!/usr/bin/python
#encoding=UTF-8


from PyQt4.QtGui import *
from PyQt4.QtCore import *

from cr.gui import crmessagebox

class TextFileEdit(QDialog):
	def __init__(self,path,encoding='utf-8',parent=None):
		super(TextFileEdit,self).__init__(parent)
		self.setWindowTitle(path)
		self.path=path
		self.encoding=encoding
		self.Layout=QVBoxLayout()
		self.SaveButton=QPushButton(_('save'))
		self.RestartButton=QPushButton(_('restart to update settings'))
		self.TextEdit=QTextEdit()
		self.TextEdit.setFrameShadow(QTextEdit.Plain)
		self.TextEdit.setText((open(self.path).read().decode(self.encoding)))
		h_layout=QHBoxLayout()
		h_layout.addWidget(self.SaveButton)
		h_layout.addWidget(self.RestartButton)
		self.Layout.addLayout(h_layout)
		self.Layout.addWidget(self.TextEdit)
		QObject.connect(self.SaveButton,SIGNAL("released()"),self.save)
		QObject.connect(self.RestartButton,SIGNAL("released()"),self.restart)
		QObject.connect(self.TextEdit,SIGNAL("textChanged()"),lambda :self.SaveButton.setEnabled(True))
		self.SaveButton.setEnabled(False)
		self.setLayout(self.Layout)
	def save(self):
		open(self.path,'w').write(unicode(self.TextEdit.toPlainText()).encode(self.encoding))
		self.SaveButton.setEnabled(False)
	def restart(self):
		crmessagebox.checkedrunning(_('Are you sure?'),CRSignal,'inner.restart')