#!/usr/bin/python
#encoding=UTF-8

import __builtin__,os,sys,webbrowser

import cr

def get_data_from_file(path):
	return open(path,'r').read()
def get_data_from_webpage(url):
	return urllib.urlopen(url).read()
def open_webpage(url):
	webbrowser.open_new_tab(url)

class Global(object):
	setting_window_size=(500,400)
	def __init__(self):
		self.initSelf()
		self.initGetText()
		self.initSignalSystem()
		self.initInnerSignals()
	def initSelf(self):
		__builtin__.CRGlobal=self
	def initGetText(self):
		self.gettext=cr.core.GetText()
		__builtin__._=self.gettext
	def initSignalSystem(self):
		self.Signal=cr.core.Signal()
		__builtin__.CRSignal=self.Signal
	def initInnerSignals(self):
		self.InnerFuncsList=[get_data_from_file,get_data_from_webpage,open_webpage]
		self.Signal.update(dict(zip(map(lambda f:"inner."+f.__name__,self.InnerFuncsList),self.InnerFuncsList)))