#!/usr/bin/python
#encoding=UTF-8

import webbrowser

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class HTMLViewer(QTextBrowser):
	def __init__(self,url='',string='',parent=None):
		super(HTMLViewer,self).__init__(parent=parent)
		if url:
			self.setWindowTitle(url)
			self.setSource(QUrl(url))
		elif string:
			self.setText(string)
		self.setOpenLinks(False)
		QObject.connect(self,SIGNAL("anchorClicked(QUrl)"),self.anchorClickedSlot)#,self,SLOT("anchorClickedSlot(QUrl)"))
	def anchorClickedSlot(self,qurl):
		url=unicode(qurl.toString())
		webbrowser.open_new_tab(url)