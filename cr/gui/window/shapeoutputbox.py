#!/usr/bin/python
#encoding=UTF-8

import random,Queue,time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from shapetool import ShapeTool
from cr.gui import crguiincrease

class ShapeOutputBox(ShapeTool):
	DEFAULT_FONT=QFont()
	def __init__(self,parent=None):
		super(ShapeOutputBox,self).__init__(parent)
		self.__wait=True
		self.__staytimer=QTimer()
		self._staytime=5000

		self._close_when_click=False
		self.__output_queue=Queue.Queue()
		QObject.connect(self.__staytimer,SIGNAL("timeout()"), self.__stopShowing)
		self._showing=False
		self.output_count=0
		self._random_move=False
		
		self._label=QLabel('', self)
		self._label.setWordWrap(True)
		self._label.setAlignment(Qt.AlignTop|Qt.AlignLeft)
		self._label.resize(self.size())
		self.setFontColor((255,255,255))
	def stop(self):
		self.__staytimer.stop()
		self.hide()
	def randomMove(self,pos1=(),pos2=()):
		if not (pos1 and pos2):
			self.move(random.randint(0,QDesktopWidget().width()-self.width()),
					random.randint(0,QDesktopWidget().height()-self.height()))
		else:
			self.move(random.randint(pos1[0],pos2[0]),random.randint(pos1[1],pos2[1]))
		
	def mousePressEvent(self,event):
		if event.button()==Qt.RightButton:self.__clicked_funcation()
		if event.button()==Qt.LeftButton:
			if self._close_when_click:self.__stopShowing()
		super(CRShapeOutputBox,self).mousePressEvent(event)
	def __stopShowing(self):
		self.hide()
		self._showing=False
		if not self.__output_queue.empty():
			s,f=self.__output_queue.get()
			self.showOutputBox(s,f)
	def isOutputQueueEmpty(self):
		return self.__output_queue.empty() and not self._showing
	def showOutputBox(self,s,f):
		self._showing=True
		self.hide()
		if self._random_move:self.randomMove()
		self.__clicked_funcation=f
		self._label.setText(s)
		self.__staytimer.start(self._staytime)
		self.show()
		self.output_count+=1
	def output(self,String,wait=True,Function=lambda *x:None):
		if self.isOutputQueueEmpty() or not wait:
			self.showOutputBox(String,Function)
		else:
			self.__output_queue.put((String,Function))
	def setFont(self,font=DEFAULT_FONT):
		self._label.setFont(QFont(font))
	def setFontColor(self,*color):
		color_=crguiincrease.getcolor(*color)
		pa=QPalette()
		pa.setColor(QPalette.WindowText,color_)
		self._label.setPalette(pa)
	def setLabelSize(self,*size):
		self._label.resize(crguiincrease.getsize(*size))
	def setLabelPos(self,*pos):
		self._label.move(crguiincrease.getpos(*pos,self=self._label,glob=self))
class ShapeOutputBoxBar(object):
	class _BoxInBar(object):
		def __init__(self,box_class,args=()):
			self.Box=box_class(*args)
		def output(self,s,func=lambda *x:None):
			self.Box.showOutputBox(s,func)
		def size(self):
			return self.Box.__output_queue__.qsize()
		def stop(self):
			self.Box.stop()
		def count(self):
			return self.Box.output_count
	def __init__(self,number,box_class,args=()):
		self.box_list=map(lambda i:self._BoxInBar(box_class,args),xrange(number))
	def output(self,s,func=lambda *x:None):
		min(self.box_list,key=lambda b:b.count()).output(s,func)
	def stop(self):
		for b in self.box_list:
			b.stop()
