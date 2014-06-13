#!/usr/bin/python
#encoding=UTF-8
import collections,types

from PyQt4.QtGui import *
from PyQt4.QtCore import *
def getsize(*size):
	if len(size)==1:
		size=size[0]
		if isinstance(size,QSize):
			size_=size
		elif isinstance(size,tuple) and len(size)==2:
			size_=QSize(*size)
		else:
			raise TypeError('size[0] must be QSize,tuple or string.')
	elif len(size)==2:
		if isinstance(size[0],int) and isinstance(size[1],int):
			size_=QSize(*size)
		else:
			raise TypeError('size[0] and size[1] must be int.')
	else:
		raise TypeError('"getsize" takes exactly 2 arguments (%d given)'%len(size))
	return size_
def getpos(*pos,**kwargs):
	if len(pos)==1:
		pos=pos[0]
		if isinstance(pos,QPoint):
			pos_=QPoint(pos)
		elif isinstance(pos,tuple) and len(pos)==2:
			pos_=QPoint(*pos)
		elif isinstance(pos,(str,unicode)):
			if 'self' in kwargs:
				self=kwargs['self']
			else:
				raise Exception('"self" must be set if "pos" is a string.')
			if 'glob' in kwargs and kwargs['glob'] is not None:
				glob=kwargs['glob']
			else:
				glob=QDesktopWidget()
			scx,scy=glob.width(),glob.height()
			sx,sy=self.width(),self.height()
			if 'l' in pos:
				px=0
			elif 'r' in pos:
				px=scx-sx
			else:
				px=(scx-sx)/2
			if 't' in pos:
				py=0
			elif 'b' in pos:
				py=scy-sy
			else:
				py=(scy-sy)/2
			pos_=QPoint(px,py)
		else:
			raise TypeError('pos[0] must be QPoint,tuple or string.')
	elif len(pos)==2:
		if isinstance(pos[0],int) and isinstance(pos[1],int):
			pos_=QPoint(*pos)
		else:
			raise TypeError('pos[0] and pos[1] must be int.')
	else:
		raise TypeError('"move" takes exactly 2 arguments (%d given)'%len(pos))
	return pos_
def addtomenu(menu,title,target,signal_system=None):
	if not signal_system:
		signal_system=CRSignal
	if callable(target):
		button=menu.addAction(_(title))
		button.triggered.connect(target)
	elif target in signal_system.getAllSignals() or isinstance(target,types.StringTypes):
		button=menu.addAction(_(title))
		button.triggered.connect(signal_system.getCaller(target))
	elif isinstance(target,collections.Iterable):
		submenu=menu.addMenu(_(title))
		for tit,tar in target:
			addtomenu(submenu,tit,tar,signal_system)
	else:
		raise Exception('%r is not a callable object , signal or a list of couple of title and efficacious target.'%target)
def transformdicttomenuformat(dic):
	return [(i,transdicttomenuformat(dic[i])) if isinstance(dic[i],dict) else (i,dic[i]) for i in dic]
def getcolor(*color):
	if len(color)==1:
		if isinstance(color[0],tuple):
			color_=QColor(*color[0])
		else:
			color_=QColor(color[0])
	elif len(color) in (3,4):
		color_=QColor(*color)
	else:
		raise TypeError('"color" must be int,str,unicode,QString,QVariant,Qt.GlobalColor,QColor or tuple include 4 or 5 int.')
	return color_		
