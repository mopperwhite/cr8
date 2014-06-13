#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
class ImageButton(QPushButton):
	def __init__(self,pic,size=(),parent=None):
		super(ImageButton,self).__init__(parent)
		if isinstance(pic,QPixmap):
			self.pixmap=pic
		else:
			self.picpath=pic
			self.pixmap=QPixmap(self.picpath)
		self.bitmap=QBitmap(self.pixmap.mask())
		self.setMask(self.bitmap)
		if size:
			self.size=size
		else:
			self.size=self.pixmap.size().width(),self.pixmap.size().height()
		self.resize(*self.size)
	def paintEvent(self,event):
		painter=QPainter(self)
		painter.drawPixmap(0,0,self.size[0],self.size[1],self.pixmap) 