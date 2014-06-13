#!/usr/bin/python
#encoding=UTF-8

import cr,time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
class CRInputWindow(cr.gui.ShapeTool):
	class _TextEdit(QTextEdit):
		def __init__(self,parent):
			self.parent=parent
			super(CRInputWindow._TextEdit,self).__init__(parent)
			self.setWindowTitle('CR')
			self.setFrameShadow(QTextEdit.Plain)

			pl=self.palette()
			pl.setBrush(QPalette.Base,QBrush(QColor(255,0,0,0)))
#			pl.setPen(QPalette.Base,QPen(QColor(255,0,0,0)))
#			pl.setColor(QPalette.Base,QColor(255,0,0,0))
			self.setPalette(pl)
			self.setStyleSheet("""border-width:0px;border-style:solid;""")
		def text(self):
			return self.toPlainText()
		def keyPressEvent(self,event):
			super(CRInputWindow._TextEdit,self).keyPressEvent(event)
			if (setting['sendbutton']['send_key']=="Ctrl+Enter" and event.modifiers()==Qt.ControlModifier and  event.key() == Qt.Key_Return) or (setting['sendbutton']['send_key']=="Enter" and event.modifiers()!=Qt.ControlModifier and  event.key() == Qt.Key_Return):
				self.parent.Send()
	def __init__(self):
		super(CRInputWindow,self).__init__(parent=None)
		if setting['window']['on_the_top']:
			invaflags=self.NOT_TOOL_FLAGS
		else:
			invaflags=self.BASE_FLAGS
		self.setting_window=cr.gui.SettingWindow(setting,env['setting_window.xml'])
		self.resize(setting['window']['size'])
		self.setBackground(env['Background.png'])
		self.setMask(env['Mask.bmp'])
		self.move(setting['window']['pos'])
		self._locked=setting['window']['lock']
		self._autohide=False
		self.setTransparency(setting['window']['nomral_transparency']/100.,
							setting['window']['mouse_on_transparency']/100.)
		self.setWindowFlags(invaflags)
		self.icon=QIcon()
		QObject.connect(self,SIGNAL("closed()"),self.close)
		self.icon.addFile(env['Icon.png'],QSize(*setting['window']['icon_size']))
		self.setWindowIcon(self.icon)
		self.initSendButton()
		self.initTextEdit()
		self.initMenu()
		self.show()
	def initSendButton(self):
		self.SendButton=cr.gui.ImageButton(env['SendButton.png'],setting['sendbutton']['size'],self)
		self.SendButton.move(*setting['sendbutton']['pos'])
		QObject.connect(self.SendButton,SIGNAL("released()"),self.Send)
	def mouseDoubleClickEvent(self,event):
		self.showMinimized()
	def initTextEdit(self):
		self.TextEdit=self._TextEdit(self)
		#self.TextEdit=QTextEdit(parent=self)
		self.TextEdit.move(*setting['textedit']['pos'])
		self.TextEdit.resize(*setting['textedit']['size'])
	def initMenu(self):
		l=[
		('operation',[
			('stop','inner.stop'),
			('clear','inner.clear'),
			]),
		('management',[
			('manage app','inner.showAppManager'),
			('manage character','inner.showCharacterManager'),
			('manage character app','inner.showCharacterAppManager'),
			]),
		('setting',[
			('manage gettext','inner.showGetTextManager'),
			('setting','inner.showSetting'),
			('input window setting',self.setting_window.show),
			]),
		('about','inner.showAbout'),
		('quit','inner.quit'),
		]
		self.updateMenu(filter(lambda i:setting['popmenu'][i[0]],l))
	def MouseMove(self,event):
		setting['window']['pos']=(self.pos().x(),self.pos().y())
		setting.save()
	def Send(self):
		s=unicode(self.TextEdit.toPlainText())
		if s:
			CRSignal('inner.reply',s)
			self.TextEdit.clear()
	def closeEvent(self,event):
		CRSignal('inner.quit')
	def showMainWindow(self):
		self.hide()
		self.show()
w=CRInputWindow()
CRSignal.connect('inner.showMainWindow',w.showMainWindow)