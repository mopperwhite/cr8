#!/usr/bin/python
#encoding=UTF-8

import sys
import cr
from PyQt4.QtGui import *
from PyQt4.QtCore import *
class MessageBoxWindow(cr.gui.ShapeOutputBox):
		def __init__(self):
			super(MessageBoxWindow,self).__init__()
			self.InitParameters()
		def InitParameters(self):
				self.resize(setting['messagebox']['window_size'])
				self.setBackground(env['Background.png'])
				self.setMask(env['Mask.bmp'])
				self._staytime=setting['messagebox']['stay_time']
				self.setLabelPos(setting['messagebox']['string_pos'])
				self.setFontColor(setting['messagebox']['string_color'])
				self.setTransparency(setting['messagebox']['nomral_transparency']/100.,
									setting['messagebox']['mouse_on_transparency']/100.)
				self._autohide=setting['messagebox']['auto_hide']
				self._close_when_click=setting['messagebox']['close_when_click']
				self._locked=setting['messagebox']['lock']
				self.move(setting['messagebox']['window_pos'])
				self.setFont(setting['messagebox']['font'])
messagebox=MessageBoxWindow()
CRSignal.connect('cr.output',messagebox.output)
CRSignal.connect('inner.output','cr.output')