#!/usr/bin/python
#encoding=UTF-8

import os,types

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import cr
from cr.gui import crguiincrease


class ShapeTool(QWidget):
	DEFAULT_FLAGS=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint | Qt.Tool
	NOT_ONTHETOP_FLAGS=Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint | Qt.Tool
	NOT_TOOL_FLAGS=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
	BASE_FLAGS=Qt.FramelessWindowHint
	def __init__(self,parent=None,signal=None,gettext=None):
		if not gettext:
			self.__gettext=_
		else:
			self.__gettext=gettext
		if not signal:
			self._signal=CRSignal
		else:
			self._signal=signal
		self.__actions=[]
		self.__menuinited=False
		super(ShapeTool,self).__init__(parent)
		self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.X11BypassWindowManagerHint|Qt.Tool)
		self._locked=False
		self._autohide=False
		self._bgdpmp=QPixmap()
		self._maskbmp=QBitmap()
		self.setTransparency()
	def setTransparency(self,nomral=1,mouse_on=1):
		self._nomral_transparency=nomral
		self._mouse_on_transparency=mouse_on
		self.setWindowOpacity(self._nomral_transparency)
		
	def __setMask(self,mask,size=None):
		mask=QBitmap(mask)
		if size==None:
			size=QSize(self.size().width(),self.size().height())
		elif isinstance(size,tuple):
			size=QSize(*size)
		self.resize(size)
		self.__maskbmp=QBitmap(mask.scaled(size))
		super(ShapeTool,self).setMask(self.__maskbmp)
		return self.__maskbmp

	def __setBackground(self,background,size=None):
		background=QPixmap(background)
		if size==None:
			size=QSize(self.size().width(),self.size().height())
		elif isinstance(size,tuple):
			size=QSize(*size)
		self.__bgpmp=QPixmap(background.scaled(size))
		palette=QPalette()
		palette.setBrush(self.backgroundRole(),QBrush(self.__bgpmp))        
		self.setPalette(palette)
		self.setAutoFillBackground=True
		return self.__bgpmp
	def setBackground(self,background,size=None):
		self._bgpmp=self.__setBackground(background,size)
	def setMask(self,mask,size=None):
		self._maskbmp=self.__setMask(mask,size)
	def addLoopAction(self,background,mask,starttime,stoptime):
		start_timer=QTimer()
		stop_timer=QTimer()
		def start():
			stop_timer.stop()
			self.__setBackground(background)
			self.__setMask(mask)
			start_timer.start(starttime)
		def stop():
			start_timer.stop()
			self.__setBackground(self._bgpmp)
			self.__setMask(self._maskbmp)
			stop_timer.start(stoptime)
		QObject.connect(start_timer,SIGNAL("timeout()"),stop)
		QObject.connect(stop_timer,SIGNAL("timeout()"),start)
		self.__actions.append(('loop',background,mask,starttime,stoptime,start_timer,stop_timer,start,stop))
		start()
	def addSignalAction(self,background,mask,signal,keeptime):
		timer=QTimer()
		def start():
			self.__setBackground(background)
			self.__setMask(mask)
			timer.start(keeptime)
		def stop():
			timer.stop()
			self.__setBackground(self._bgpmp)
			self.__setMask(self._maskbmp)
		QObject.connect(timer,SIGNAL("timeout()"),stop)
		self._signal.connect(signal,start)
		self.__actions.append(('signal',background,mask,signal,keeptime,timer,start,stop))
	def mousePressEvent(self,event):  
		if event.button()==Qt.LeftButton:
			if self._locked:return
			self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()  
			event.accept()
		
	def mouseMoveEvent(self,event):  
		if event.buttons() == Qt.LeftButton:
			if self._locked:
				return
			super(ShapeTool,self).move(event.globalPos()-self.dragPosition)  
			event.accept()
	def enterEvent(self,event):  
		if self._autohide:
			self.__hide=QTimer()
			QObject.connect(self.__hide,SIGNAL("timeout()"), self.__showWhenMouseOut)
			self.__hide.start(50)
			self.hide()
		else:
		    self.setWindowOpacity(self._mouse_on_transparency)
	def leaveEvent(self,event):
		if not self._autohide:self.setWindowOpacity(self._nomral_transparency)
	def __showWhenMouseOut(self):		
		if not self.mask().contains(QPoint(QCursor.pos().x()-self.x(),QCursor.pos().y()-self.y())):
			del self.__hide
			self.show()	


	def __showContextMenu(self, pos):
		self.contextMenu.move(self.pos() + pos)
		self.contextMenu.show()
	def addMenuItem(self,title,target):
		if not self.__menuinited:
			self.setContextMenuPolicy(Qt.CustomContextMenu)
			self.customContextMenuRequested.connect(self.__showContextMenu)
			self.contextMenu=QMenu(self)
			self.__menuinited=True
		crguiincrease.addtomenu(self.contextMenu,title,target,self._signal)
	def updateMenu(self,lis):
		for title,target in lis:
			self.addMenuItem(self.__gettext(title),target)
	def resize(self,*size):
		super(ShapeTool,self).resize(crguiincrease.getsize(*size))
	def move(self,*pos):
		super(ShapeTool,self).move(crguiincrease.getpos(*pos,self=self))
	
