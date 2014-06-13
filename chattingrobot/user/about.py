#!/usr/bin/python
#encoding=UTF-8
import webbrowser

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
class AboutWindow(QDialog):
	def __init__(self,parent=None):
		super(AboutWindow,self).__init__(parent)
		self.setWindowTitle(_('about'))

		self.layout=QVBoxLayout(self)

		self.pages_layout=QHBoxLayout()

		self.about_textedit=cr.gui.HTMLViewer(CRGlobal.init_path['local']['about'])
		self.warning_textedit=cr.gui.HTMLViewer(CRGlobal.init_path['local']['warning'])
		self.pages_layout.addWidget(self.about_textedit)
		self.pages_layout.addWidget(self.warning_textedit)		
		self.layout.addLayout(self.pages_layout)

		self.buttons_layout=QHBoxLayout()
		self.aboutqt_button=QPushButton(_('about Qt'))
		self.show_about_in_webbrowser_button=QPushButton(_('show %s page in webbrowser',_('about')))
		self.show_warning_in_webbrowser_button=QPushButton(_('show %s page in webbrowser',_('warning')))
		QObject.connect(self.aboutqt_button,SIGNAL("released()"),QApplication.aboutQt)
		QObject.connect(self.show_about_in_webbrowser_button,SIGNAL("released()"),self.getopener(CRGlobal.init_path['local']['about']))
		QObject.connect(self.show_warning_in_webbrowser_button,SIGNAL("released()"),self.getopener(CRGlobal.init_path['local']['warning']))
		self.buttons_layout.addWidget(self.aboutqt_button)
		self.buttons_layout.addWidget(self.show_about_in_webbrowser_button)
		self.buttons_layout.addWidget(self.show_warning_in_webbrowser_button)
		self.layout.addLayout(self.buttons_layout)
	def getopener(self,url):
		def opener():
			webbrowser.open_new_tab(url)
		return opener
