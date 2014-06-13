#!/usr/bin/python
#encoding=UTF-8

import sys,json

import cr
class CharacterWindow(cr.gui.ShapeTool):
	def __init__(self,parent):
		self.parent_=parent
		super(CharacterWindow,self).__init__(None,parent.signal)
		self.InitParameters()
		self.InitMenu()
		self.show()
	def InitParameters(self):

		self.resize(self.parent_.setting['window']['window_size'])
		self.move(self.parent_.setting['window']['window_pos'])
		self._locked=self.parent_.setting['window']['lock']
		self._autohide=self.parent_.setting['window']['auto_hide']
		self.setTransparency(self.parent_.setting['window']['nomral_transparency']/100.0,
							self.parent_.setting['window']['mouse_on_transparency']/100.0)
		self.setBackground(self.parent_.path['window']['picture'])
		self.setMask(self.parent_.path['window']['mask'])
	def changeLock(self):
		self._locked=not self._locked
	def InitMenu(self):
		dl=cr.gui.crguiincrease.transformdicttomenuformat(json.load(open(self.parent_.path['window']['menu'])))
		l=[
		('teach','character.teach'),
			('setting',[
			('app manager','character.showAppManager'),
			('setting',self.parent_.setting_window.show),
			('edit character files',self.parent_.path_edit.show),]),
		('lock/unlock',self.changeLock),
		('show main window','inner.showMainWindow'),
		('quit','inner.quit'),
		]
		self.updateMenu(dl+l)
	def mouseMoveEvent(self,event):
		super(CharacterWindow,self).mouseMoveEvent(event)
		self.parent_.setting['window']['window_pos']=(self.pos().x(),self.pos().y())
		self.parent_.setting.save()
	def leaveEvent(self,event):
		super(CharacterWindow,self).leaveEvent(event)
		self.parent_.setting['window']['window_pos']=(self.pos().x(),self.pos().y())
		self.parent_.setting.save()
	def mouseDoubleClickEvent(self,event):
		self.parent_.signal('character.double_clicked',event.x(),event.y())
	def mouseReleaseEvent(self,event):
		self.parent_.signal('character.clicked',event.x(),event.y())