#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
from cr.gui import crmessagebox
from errormessagebox import ErrorMessageBox

class SignalDialog(QDialog):
	def __init__(self,signal_system,default_signal='',default_args=(),hasargs=True,title='select signal',parent=None):
		super(SignalDialog,self).__init__(parent)
		self.setWindowTitle(_(title))
		self.default_signal=default_signal
		self.default_args=default_args
		self.signal_system=signal_system
		cr.core.crtry.checktype('signal_system',signal_system,cr.core.Signal)
		cr.core.crtry.checktype('default_args',default_args,tuple)
		self.layout=QVBoxLayout()

		self.signal_label=QLabel()
		self.layout.addWidget(self.signal_label)

		input_signal_layout=QHBoxLayout()
		input_signal_layout.addWidget(QLabel(_('input signal')))
		self.input_signal_textedit=QLineEdit()
		QObject.connect(self.input_signal_textedit,SIGNAL("textChanged(QString)"),self.__getSignalFromLineEdit)
		input_signal_layout.addWidget(self.input_signal_textedit)
		self.layout.addLayout(input_signal_layout)

		select_signal_layout=QHBoxLayout()
		select_signal_layout.addWidget(QLabel(_('select signal')))
		self.select_signal_combobox=QComboBox()
		QObject.connect(self.select_signal_combobox,SIGNAL("currentIndexChanged(int)"),self.__getSignalFromComboBox)
		self.select_signal_combobox.addItems(['']+self.signal_system.getAllSignals())
		select_signal_layout.addWidget(self.select_signal_combobox)
		self.layout.addLayout(select_signal_layout)

		input_args_layout=QHBoxLayout()
		input_args_layout.addWidget(QLabel(_('input args')))
		self.input_args_textedit=QLineEdit()
		input_args_layout.addWidget(self.input_args_textedit)
		self.layout.addLayout(input_args_layout)

		self.button_box=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		self.layout.addWidget(self.button_box)
		QObject.connect(self.button_box.button(QDialogButtonBox.Cancel), SIGNAL("clicked()"), self, SLOT("close()"))
		QObject.connect(self.button_box.button(QDialogButtonBox.Ok), SIGNAL("clicked()"), self.__ok)


		self.setLayout(self.layout)
		self.signal=unicode(default_signal)
		self.setArgs(default_args)
		if not hasargs:self.input_args_textedit.setEnabled(False)


	def setArgs(self,a):
		self.input_args_textedit.setText(repr(a))
		self.args=a
	def __getSignalFromLineEdit(self):
		self.signal=unicode(self.input_signal_textedit.text())
		self.signal_label.setText(self.input_signal_textedit.text())
		i=self.select_signal_combobox.findText(self.input_signal_textedit.text())
		if i==-1:
			self.select_signal_combobox.setCurrentIndex(0)
		else:
			self.select_signal_combobox.setCurrentIndex(i)
	def __getSignalFromComboBox(self):
		self.signal=unicode(self.select_signal_combobox.currentText())
		self.signal_label.setText(self.select_signal_combobox.currentText())
		self.input_signal_textedit.setText(self.select_signal_combobox.currentText())
	def __getArgsFromLineEdit(self):
		try:
			o=eval(unicode(self.input_args_textedit.text()))
		except:
			emb=ErrorMessageBox('Args Error','Invalid statement.',cr.core.crtry.gettraceback(),self)
			emb.exec_()
			return False
		if not isinstance(o,tuple):
			crmessagebox.warning(_('Args must be tuple.'),parent=self)
			return False
		else:
			self.args=o
			return True
	def __ok(self):
		if not self.__getArgsFromLineEdit():return 
		if self.signal and self.signal not in self.signal_system.getAllSignals() and not crmessagebox.checkedwarning('This signal is not connected,continue anyway?',self):return
		self.close()
	def get(self):
		self.exec_()
		return cr.core.Messager(self.signal,self.args,signal=self.signal,args=self.args)