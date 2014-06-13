#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from basesetting import SettingWindowTab
from cr.gui import crmessagebox,CoupleDialog
import cr
class GetTextManager(QDialog):
	class _BaseTabItem(QWidget):
		def __init__(self,parent,id,mark):
			super(GetTextManager._BaseTabItem,self).__init__()
			self.parent_=parent
			self.id=id
			self.layout=QHBoxLayout(self)
#			self.label=QLabel(self.id)
			self.label=QLineEdit(self.id)
			self.label.setReadOnly(True)
			self.lineedit=QLineEdit()
			self.add_button=QPushButton(_(mark))
			self.layout.addWidget(self.label)
			self.layout.addWidget(self.lineedit)
			self.layout.addWidget(self.add_button)
			QObject.connect(self.add_button,SIGNAL('released()'),self.__buttonClicked)
			QObject.connect(self.add_button,SIGNAL("editingFinished()"),self.__editingFinished)
		def __buttonClicked(self):
			s=unicode(self.lineedit.text())
			if s:self.buttonClicked(s)
		def buttonClicked(self,s):pass
		def __editingFinished(self):
			self.__editingFinished(unicode(self.lineedit.text()))
		def editingFinished(self,s):pass
	class _AllTabItem(_BaseTabItem):
		def __init__(self,parent,id):
			super(GetTextManager._AllTabItem,self).__init__(parent,id,'add')
		def buttonClicked(self,s):
			self.parent_.addExistItem(self.id,s)
			self.close()
	class _ExistTabItem(_BaseTabItem):
		def __init__(self,parent,id,value):
			super(GetTextManager._ExistTabItem,self).__init__(parent,id,'delete')
			self.lineedit.setText(value)
		def buttonClicked(self,s):
			self.parent_.removeExistItem(self.id)
			self.close()
		def save(self):
			s=unicode(self.lineedit.text())
			if s:
				self.parent_.gettext.add(self.id,s)
			else:
				self.parent_.gettext.remove(self.id)
	def __init__(self,gettext=None,parent=None):
		super(GetTextManager,self).__init__(parent)
		if gettext==None:
			self.gettext=_
		else:
			cr.core.crtry.checktype('gettext',gettext,cr.core.GetText)
			self.gettext=gettext
		self.couplt_dialog=CoupleDialog('new entry','id','string',self)
		self.__initWindow()
	def __initWindow(self):
		
		self.setWindowTitle(_('GetText Manager'))
		self.layout=QVBoxLayout(self)
		self.__initButtons()
		self.tab_widget=QTabWidget()
		self.layout.addWidget(self.tab_widget)
		self.__initExistTab()
		self.__initAllTab()
	def __initButtons(self):
		self.buttons_layout=QHBoxLayout()
		self.save_button=QPushButton(_('save'))
		self.new_entry_button=QPushButton(_('new entry'))
		self.restart_button=QPushButton(_('restart to update settings'))
		QObject.connect(self.save_button,SIGNAL("released()"),self.save)
		QObject.connect(self.new_entry_button,SIGNAL("released()"),self.new_entry)
		QObject.connect(self.restart_button,SIGNAL("released()"),self.restart)
		self.buttons_layout.addWidget(self.save_button)
		self.buttons_layout.addWidget(self.new_entry_button)
		self.buttons_layout.addWidget(self.restart_button)
		self.layout.addLayout(self.buttons_layout)
	def __initExistTab(self):
		self.exist_tab=self.addTab(_('existing entries'))
		self.exist_tab_dic={}
		exist_list=self.gettext.items()
		exist_list.sort()
		for i,v in exist_list:
			t=self._ExistTabItem(self,i,v)
			self.exist_tab.add(t)
			self.exist_tab_dic[i]=t
	def __initAllTab(self):
		self.all_tab=self.addTab(_('all entries'))
		all_list=list(self.gettext.record-set(self.gettext.keys())-set(self.gettext.values()))
		all_list.sort()
		for i in all_list:
			self.all_tab.add(self._AllTabItem(self,i))
	def addTab(self,title):
		tab=SettingWindowTab()
		self.tab_widget.addTab(tab,title)
		return tab
	def save(self):
		for t in self.exist_tab_dic.itervalues():
			t.save()
		if not self.gettext.save(True):
			crmessagebox.warning(_('Cannot save GetText.'),self)
	def restart(self):
		crmessagebox.checkedrunning(_('Are you sure?'),CRSignal,'inner.restart')
	def new_entry(self):
		r=self.couplt_dialog.get()
		if r:
			i,s=r 
			self.addExistItem(i,s)
	def addExistItem(self,id,s):
		self.gettext.add(id,s)
		t=self._ExistTabItem(self,id,s)
		self.exist_tab_dic[id]=t
		self.exist_tab.add(t)
	def removeExistItem(self,id):
		self.gettext.remove(id)
		del self.exist_tab_dic[id]
		if id in self.gettext.record:
			self.all_tab.add(self._AllTabItem(self,id))