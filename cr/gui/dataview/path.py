#!/usr/bin/python
#encoding=UTF-8

import os,shutil

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
from basesetting import BaseSettingWindow

class PathEdit(BaseSettingWindow):
	class _BasePathWidget(QWidget):
		def __init__(self,title,path,parent=None):
			super(PathEdit._BasePathWidget,self).__init__(parent)
			self.path=path
			self.layout=QHBoxLayout(self)
			self.title_label=QLabel(_(title))
			self.path_label=QLineEdit(path)
			self.path_label.setReadOnly(True)
			self.filedialog=QFileDialog()
			self.button=QPushButton(_('select'))
			QObject.connect(self.button,SIGNAL("released()"),self.select)
			self.layout.addWidget(self.title_label)
			self.layout.addWidget(self.path_label)
			self.layout.addWidget(self.button)
		def setPath(self,p):
			if p:
				self.path_label.setText(p)
				self.path=unicode(p)
		def select(self):pass
	class _FilePathWidget(_BasePathWidget):
		def select(self):
			self.setPath(self.filedialog.getOpenFileName())
	class _DirPathWidget(_BasePathWidget):
		def select(self):
			self.setPath(self.filedialog.getExistingDirectory())
	def __init__(self,path,parent=None):
		super(PathEdit,self).__init__(path,parent)
		cr.core.crtry.checktype('path',path,cr.core.Path)
		self.path=path
		self.list=[]
		self.__initWindow()
	def __initWindow(self):
		for i in self.path.iterkeys():
			tab=self.addTab(_(i))
			for j in self.path[i].iterkeys():
				tab.add(self.getWidget(_(j),self.path[i][j]))
	def getWidget(self,title,p):
		if os.path.exists(p):
			if os.path.isfile(p):
				w=self._FilePathWidget(title,p)
				flag='file'
			elif os.path.isdir(p):
				w=self._DirPathWidget(title,p)
				flag='dir'
			else:
				raise OSError('Unknown path %r.'%p)
		else:
			raise IOError('No such file or directory:%r'%p)
		self.list.append((w,flag,p))
		return w
	def save(self):
		for w,f,p in self.list:
			if w.path!=p:
				if f=='file':
					shutil.copyfile(w.path,p)
				elif f=='dir':
					shutil.copytree(w.path,p)