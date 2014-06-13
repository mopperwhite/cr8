#!/usr/bin/python
#encoding=UTF-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os,traceback
import cr
from basesetting import BaseSettingWindow

class BaseSettingWidget(QWidget):
	def __init__(self,title,dic,pk,key,parent=None):
		QWidget.__init__(self,parent)
		self.parent_=parent
		self.__dic=dic
		self.pk=pk
		self.key=key
		self.Layout=QHBoxLayout(self)
		self.title=title
		self.__label=QLabel(title)
#		self.__label.setEnabled(False)
#		self.__label.setReadOnly(True)
		self.Layout.addWidget(self.__label)
		self.value=self.__dic[self.pk][self.key]
	def addItem(self,w):
		self.Layout.addWidget(w)
	def setValue(self,v):
		self.__dic[self.pk][self.key]=v
		self.value=v
	def getValue(self):
		return self.value

class StrWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.LineEdit=QLineEdit()
		self.LineEdit.setText(dic[pk][key])
		self.addItem(self.LineEdit)
		QObject.connect(self.LineEdit, SIGNAL("textEdited(QString)"), self.editFinished)
	def editFinished(self):
		self.setValue(unicode(self.LineEdit.text()))

class BoolWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.CheckBox=QCheckBox()
		self.CheckBox.setChecked(self.getValue())
		self.addItem(self.CheckBox)
		self.connect(self.CheckBox,SIGNAL("clicked()"),self.save)
	def save(self):
		self.setValue(self.CheckBox.isChecked())

class ColorWidget(BaseSettingWidget):
	MaxSize=(50,20)
	def __init__(self,title,dic,pk,key,parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent=None)
		self.ColorDialog=QColorDialog()
		self.Label=QLabel()
		self.Label.setMaximumSize(*self.MaxSize)
		self.setColor()
		self.Button=QPushButton(_('select color'))
		self.connect(self.Button,SIGNAL("clicked()"),self.selectColor)
		self.addItem(self.Label)
		self.addItem(self.Button)
	def setColor(self):
		self.pix=QPixmap(self.Label.size())
		painter=QPainter(self.pix)
		painter.setBrush(QBrush(QColor(*self.getValue()),Qt.SolidPattern))
		painter.drawRect(0,0,self.Label.width(),self.Label.height())
		self.Label.setPixmap(self.pix)
	def selectColor(self):
		color=self.ColorDialog.getColor(QColor(*self.getValue()))
		self.setValue((color.red(),color.green(),color.blue()))
		self.setColor()

class ComboBox(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,list_,parent=None):
		super(ComboBox,self).__init__(title,dic,pk,key,parent)
		self.dic=dict((_(i),i) for i in list_)
		self.list=list_
		self.combobox=QComboBox()
		self.combobox.addItems(self.dic.keys())
		self.combobox.setCurrentIndex(self.combobox.findText(_(self.getValue())))
		self.addItem(self.combobox)
		QObject.connect(self.combobox,SIGNAL("currentIndexChanged(int)"),self.currentIndexChanged)
	def currentIndexChanged(self):
		self.setValue(self.dic[unicode(self.combobox.currentText())])

class DoubleWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,rang,suffix='',parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.SpinBox=QDoubleSpinBox()
		self.SpinBox.setRange(rang[0],rang[1])
		self.SpinBox.setSuffix(suffix)
		self.SpinBox.setValue(dic[pk][key])
		self.addItem(self.SpinBox)
		QObject.connect(self.SpinBox, SIGNAL("valueChanged(int)"), self.editFinished)
	def editFinished(self):
		self.setValue(self.SpinBox.value())

class ParentFileWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,
				caption='',
				_dir='.',_filter=[],
				selectedFilter='',
				dir_only=False,
				plural_paths=False,
				parent=None):
		if not caption:caption=_('select file')
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent=None)
		self.caption=caption
		self.dir=_dir
		self.filter=';;'.join(_filter)
		self.selectedFilter=selectedFilter
		self.dir_only=dir_only
		self.plural_paths=plural_paths
		
		self.FileDialog=QFileDialog()
		if self.dir_only:self.FileDialog.setOption(QFileDialog.Option())
		
		
		self.Label=QLabel()
		self.updateLabel()
		
		self.Button=QPushButton(self.caption)
		if dir_only:
			self.connect(self.Button,SIGNAL("clicked()"),self.selectDir)
		elif not self.plural_paths:
			self.connect(self.Button,SIGNAL("clicked()"),self.selectFile)
		else:
			self.connect(self.Button,SIGNAL("clicked()"),self.selectFiles)
		self.addItem(self.Label)
		self.addItem(self.Button)
	def selectFile(self):
		self.setValue(unicode(
				self.FileDialog.getOpenFileName(
						caption=self.caption,
						directory=self.dir,
						filter=self.filter,
						selectedFilter=self.selectedFilter)))
		self.updateLabel()
	def selectFiles(self):
		self.setValue(map(unicode,
				self.FileDialog.getOpenFileNames(
						caption=self.caption,
						directory=self.dir,
						filter=self.filter,
						selectedFilter=self.selectedFilter)))
		self.updateLabel()
	def selectDir(self):
		self.setValue(unicode(
				self.FileDialog.getExistingDirectory(
						caption=self.caption,
						directory=self.dir,)))
		self.updateLabel()
	
	def updateLabel(self):
		if not self.plural_paths:
			self.Label.setText(self.getValue())
		else:
			self.Label.setText('\n'.join(self.getValue()))
class FileWidget(ParentFileWidget):
	def __init__(self,title,dic,pk,key,
				dir='.',filter=[],
				selectedFilter='',
				parent=None):
		ParentFileWidget.__init__(self,title,dic,pk,key,
				caption=_('select file'),
				_dir=dir,_filter=filter,
				selectedFilter=selectedFilter,
				dir_only=False,
				plural_paths=False,
				parent=parent)
class FilesWidget(ParentFileWidget):
	def __init__(self,title,dic,pk,key,
				dir='.',filter=[],
				selectedFilter='',
				parent=None):
		ParentFileWidget.__init__(self,title,dic,pk,key,
				caption=_('select files'),
				_dir=dir,_filter=filter,
				selectedFilter=selectedFilter,
				dir_only=False,
				plural_paths=True,
				parent=parent)
class DirWidget(ParentFileWidget):
	def __init__(self,title,dic,pk,key,
				dir='.',filter=[],
				selectedFilter='',
				parent=None):
		ParentFileWidget.__init__(self,title,dic,pk,key,
				caption=_('select directory'),
				_dir=dir,_filter=filter,
				selectedFilter=selectedFilter,
				dir_only=True,
				plural_paths=False,
				parent=parent)


class FontWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent=None)
		
		self.Font=QFont()
		self.Font.fromString(self.getValue())
		
		self.FontDialog=QFontDialog()
		self.FontDialog.setFont(self.Font)
		
		self.Button=QPushButton(_('select font'))
		self.connect(self.Button,SIGNAL("clicked()"),self.selectFont)
		
		self.Label=QLabel()
		self.updateLabel()
		
		self.addItem(self.Label)
		self.addItem(self.Button)
	def updateLabel(self):
		self.Label.setFont(self.Font)
		self.Label.setText(u"%s %d"%(self.Font.family(),self.Font.pointSize()))
	def selectFont(self):
		self.Font,b=self.FontDialog.getFont(self.Font)
		self.updateLabel()
		self.setValue(unicode(self.Font.toString()))


class IntWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,rang,suffix='',parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.SpinBox=QSpinBox()
		self.SpinBox.setRange(*rang)
		self.SpinBox.setSuffix(suffix)
		self.SpinBox.setValue(self.getValue())
		self.addItem(self.SpinBox)
		QObject.connect(self.SpinBox, SIGNAL("valueChanged(int)"), self.editFinished)
	def editFinished(self):
		self.setValue(self.SpinBox.value())

class PasswdWidget(StrWidget):
	def __init__(self,title,dic,pk,key,parent=None):
		StrWidget.__init__(self,title,dic,pk,key,parent)
		self.LineEdit.setEchoMode(QLineEdit.Password)

class PosWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,x_rang,y_rang,parent=None):
		self._DirectionNameList=['user-defined','left','right','top','bottom','lefttop','righttop','leftbottom','rightbottom','center']
		self.DirectionNameList=map(_,self._DirectionNameList)
		self.DirectionShortNameList=['',       'l',    'r',    't',  'b',     'lt',     'rt',      'lb',        'rb',         'c'    ]
		self.DirectionShortNameDict=dict(zip(self.DirectionNameList,self.DirectionShortNameList))
		self.DirectionNameCheckDict=dict(zip(self.DirectionShortNameList,self.DirectionNameList))
		self.ComboBoxMaxVisibleItems=10
		
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.x_rang,self.y_rang=x_rang,y_rang
		self.InitSpinBox()
		self.InitComboBox()
		self.CheckValue()
	def InitSpinBox(self):
		self.XSpinBox=QSpinBox()
		self.YSpinBox=QSpinBox()
		self.XSpinBox.setSuffix(_('px'))
		self.YSpinBox.setSuffix(_('px'))
		self.XSpinBox.setRange(*self.x_rang)
		self.YSpinBox.setRange(*self.y_rang)
		self.addItem(self.XSpinBox)
		self.addItem(self.YSpinBox)
		self.connect(self.XSpinBox,SIGNAL("valueChanged(int)"), self.editSpinBox)
		self.connect(self.YSpinBox,SIGNAL("valueChanged(int)"), self.editSpinBox)
	def InitComboBox(self):
		self.ComboBox=QComboBox()
		self.ComboBox.addItems(self.DirectionNameList)
		self.ComboBox.setMaxVisibleItems(self.ComboBoxMaxVisibleItems)
		self.addItem(self.ComboBox)
		self.connect(self.ComboBox,SIGNAL("currentIndexChanged(int)"),self.ComboBoxChanged)
	def CheckValue(self):
		if type(self.getValue()) in (str,unicode):
			if 'c' in self.getValue():self.ComboBox.setCurrentIndex(self.DirectionNameList.index(self.DirectionNameCheckDict['c']))
			else:
				if 'l' in self.getValue():LR='l'
				elif 'r' in self.getValue():LR='r'
				else:LR=''
				if 't' in self.getValue():TB='t'
				elif 'b' in self.getValue():TB='b'
				else:TB=''
				self.ComboBox.setCurrentIndex(self.DirectionNameList.index(self.DirectionNameCheckDict[LR+TB]))
		else:
			x,y=self.getValue()
			self.XSpinBox.setValue(x)
			self.YSpinBox.setValue(y)
	def ComboBoxChanged(self):
		if self.DirectionShortNameDict[unicode(self.ComboBox.currentText())]:self.setValue(self.DirectionShortNameDict[unicode(self.ComboBox.currentText())])
		else:self.setValue((self.XSpinBox.value(),self.YSpinBox.value()))
	def editSpinBox(self):
		self.setValue((self.XSpinBox.value(),self.YSpinBox.value()))
		self.ComboBox.setCurrentIndex(self.DirectionNameList.index(self.DirectionNameCheckDict['']))

class SizeWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,w_rang,h_rang,parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.w_rang,self.h_rang=w_rang,h_rang
		self.InitSpinBox()
		self.CheckBox=QCheckBox(_('scale'))
		self.CheckBox.setChecked(True)
		self.addItem(self.CheckBox)
	def InitSpinBox(self):
		self.WSpinBox=QSpinBox()
		self.HSpinBox=QSpinBox()
		self.BeingEditedSpin=''
		self.W,self.H=self.getValue()
		self.WSpinBox.setRange(*self.w_rang)
		self.HSpinBox.setRange(*self.h_rang)
		self.WSpinBox.setSuffix(_('px'))
		self.HSpinBox.setSuffix(_('px'))
		w,h=self.getValue()
		self.WSpinBox.setValue(w)
		self.HSpinBox.setValue(h)
		self.addItem(self.WSpinBox)
		self.addItem(self.HSpinBox)
		self.connect(self.WSpinBox,SIGNAL("editingFinished()"),self.StopBeingEdited)
		self.connect(self.HSpinBox,SIGNAL("editingFinished()"),self.StopBeingEdited)
		self.connect(self.WSpinBox,SIGNAL("valueChanged(int)"),self.WStartBeingEdited)
		self.connect(self.HSpinBox,SIGNAL("valueChanged(int)"),self.HStartBeingEdited)
	def WStartBeingEdited(self):
		if not self.BeingEditedSpin:self.BeingEditedSpin="LEFT"
		if self.BeingEditedSpin=="LEFT":
			if self.CheckBox.isChecked():
				self.HSpinBox.setValue(float(self.WSpinBox.value())/self.W*self.H)
	def HStartBeingEdited(self):
		if not self.BeingEditedSpin:self.BeingEditedSpin="RIGHT"
		if self.BeingEditedSpin=="RIGHT":
			if self.CheckBox.isChecked():
				self.WSpinBox.setValue(float(self.HSpinBox.value())/self.H*self.W)
	def StopBeingEdited(self):
		self.BeingEditedSpin=""
		self.W,self.H=self.WSpinBox.value(),self.HSpinBox.value()
		self.setValue((self.W,self.H))
class UnknownWidget(BaseSettingWidget):
	def __init__(self,title,dic,pk,key,parent=None):
		BaseSettingWidget.__init__(self,title,dic,pk,key,parent)
		self.LineEdit=QLineEdit()
		self.LineEdit.setText(repr(dic[pk][key]))
		self.addItem(self.LineEdit)
		QObject.connect(self.LineEdit, SIGNAL("textEdited(QString)"), self.editFinished)
	def editFinished(self):
		if not crtry.run(lambda :self.setValue(eval(unicode(self.LineEdit.text())))):
			QMessageBox.warning(None,_('error'),_('Cannot save the value named %s (%s).',self.title,unicode(self.LineEdit.text())))


def VALUES_FORMAT_DICT():
	return {
			u'$SCREEN_WIDTH':unicode(QDesktopWidget().width()),
			u'$SCREEN_HEIGHT':unicode(QDesktopWidget().height()),
			}
def VALUES_REFORMAT_DICT():
	return dict(zip(VALUES_FORMAT_DICT().values(),VALUES_FORMAT_DICT().keys()))
def TRANSFORM_DICT():
	return {
'Int':lambda dic1,pk,k,dic2,parent=None:IntWidget(_(k),dic1,pk,k,dic2[k]['range'],dic2[k]['suffix'],parent=parent),
'Double':lambda dic1,pk,k,dic2,parent=None:DoubleWidget(_(k),dic1,pk,k,dic2[k]['range'],dic2[k]['suffix'],parent=parent),
'Str':lambda dic1,pk,k,dic2,parent=None:StrWidget(_(k),dic1,pk,k,parent=parent),
'Pos':lambda dic1,pk,k,dic2,parent=None:PosWidget(_(k),dic1,pk,k,dic2[k]['x_range'],dic2[k]['y_range'],parent=parent),
'Size':lambda dic1,pk,k,dic2,parent=None:SizeWidget(_(k),dic1,pk,k,dic2[k]['w_range'],dic2[k]['h_range'],parent=parent),
'Bool':lambda dic1,pk,k,dic2,parent=None:BoolWidget(_(k),dic1,pk,k,parent=parent),
'Color':lambda dic1,pk,k,dic2,parent=None:ColorWidget(_(k),dic1,pk,k,parent=parent),
'Font':lambda dic1,pk,k,dic2,parent=None:FontWidget(_(k),dic1,pk,k,parent=parent),
'File':lambda dic1,pk,k,dic2,parent=None:FileWidget(_(k),dic1,pk,k,dir=dic2[k]['dir'],filter=dic2[k]['filter'],selectedFilter=dic2[k]['selected_filter'],parent=parent),
'Files':lambda dic1,pk,k,dic2,parent=None:FileWidget(_(k),dic1,pk,k,dir=dic2[k]['dir'],filter=dic2[k]['filter'],selectedFilter=dic2[k]['selected_filter'],parent=parent),
'Dir':lambda dic1,pk,k,dic2,parent=None:DirWidget(_(k),dic1,pk,k,dir=dic2[k]['dir'],parent=parent),
'Passwd':lambda dic1,pk,k,dic2,parent=None:PasswdWidget(_(k),dic1,pk,k,parent=parent),
'Unknown':lambda dic1,pk,k,dic2,parent=None:UnknownWidget(_(k),dic1,pk,k,parent=parent),
'Combo':lambda dic1,pk,k,dic2,parent=None:ComboBox(_(k),dic1,pk,k,dic2[k]['items'].split(dic2[k]['sep']),parent=parent),
}
def format_values(s):
	return reduce(lambda x,y:x.replace(y,VALUES_FORMAT_DICT()[y]),[cr.core.crpath.format(s)]+VALUES_FORMAT_DICT().keys())
def reformat_values(s):
	return reduce(lambda x,y:x.replace(y,VALUES_REFORMAT_DICT()[y]),[cr.core.crpath.reformat(s)]+VALUES_FORMAT_DICT().keys())
class SettingWindow(BaseSettingWindow):
	def __init__(self,setting,setting_path,parent=None):
		super(SettingWindow,self).__init__(setting,parent)
		sp_dic=cr.core.XmlSetting(setting_path,format_values,reformat_values)
		for i in sp_dic.getAttrib()["order"].split(sp_dic.getAttrib()["sep"]):
			tab=self.addTab(_(i))
			dic=sp_dic[i]
			for j in dic.getAttrib()["order"].split(dic.getAttrib()["sep"]):
				try:
					func=TRANSFORM_DICT()[dic[j]['type']]
				except:
					func=TRANSFORM_DICT()["Unknown"]
				tab.add(func(self.setting,i,j,dic,self))