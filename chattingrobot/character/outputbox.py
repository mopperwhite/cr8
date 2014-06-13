#!/usr/bin/python
#encoding=UTF-8

import cr
class OutputBox(cr.gui.ShapeOutputBox):
	def __init__(self,parent):
		self.parent_=parent
		super(OutputBox,self).__init__(None)
		self._random_move=True
		self.InitParameters()
	def InitParameters(self):

		self._staytime=self.parent_.setting['output']['stay_time']
		self.setLabelPos(self.parent_.setting['output']['string_pos'])
		self.setFontColor(self.parent_.setting['output']['string_color'])
		self.setTransparency(self.parent_.setting['output']['nomral_transparency']/100.,
						self.parent_.setting['output']['mouse_on_transparency']/100.)
		self._autohide=self.parent_.setting['output']['auto_hide']
		self._close_when_click=self.parent_.setting['output']['close_when_click']
		self._locked=self.parent_.setting['output']['lock']
		self.resize(self.parent_.setting['output']['window_size'])
		self.Pos1=self.parent_.setting['output']['pos1']
		self.Pos2=self.parent_.setting['output']['pos2']
		self.setFont(self.parent_.setting['output']['font'])
		self.setBackground(self.parent_.path['output']['background'])
		self.setMask(self.parent_.path['output']['mask'])
	def randomMove(self):
		xp,yp=self.parent_.setting['window']['window_pos']
		x1,y1=self.Pos1
		x2,y2=self.Pos2
		x1,x2=min(x1,x2),max(x1,x2)
		y1,y2=min(y1,y2),max(y1,y2)
		super(OutputBox,self).randomMove((xp+x1,yp+y1),(xp+x2,yp+y2))
	def mouseDoubleClickEvent(self,event):
		self.parent_.signal('character.outputbox.double_clicked',event.x(),event.y())
	def mouseReleaseEvent(self,event):
		self.parent_.signal('character.outputbox.clicked',event.x(),event.y())
class OutputBar(cr.gui.ShapeOutputBoxBar):
	def __init__(self,parent):
		super(OutputBar,self).__init__(parent.setting['output']['boxes_number'],OutputBox,(parent,))
