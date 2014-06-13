#!/usr/bin/python
#encoding=UTF-8

import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from app import AppManager
import cr
from cr.core.datamodel.basedatabase import ARGS_MODE_FLAGS
class DatabaseAdvancedEdit(QMainWindow):
	class _EntryWidget(QWidget):
		def __init__(self,entry,unit):
			super(DatabaseAdvancedEdit._EntryWidget,self).__init__()
			self.unit=unit
			self.entry=entry
			self.main_layout=QVBoxLayout(self)
			self.lineedit=QLineEdit()
			self.main_layout.addWidget(self.lineedit)
			self.layout=QHBoxLayout()
			self.main_layout.addLayout(self.layout)
			self.__initLeftList()
			self.__initRightList()
			self.__initButtons()
		def __initLeftList(self):
			self.left_layout=QVBoxLayout()
			self.layout.addLayout(self.left_layout)
			self.left_addButton=QPushButton(_('add'))
			self.left_deleteButton=QPushButton(_('delete'))
			self.left_list=QListWidget()
			self.left_layout.addWidget(self.left_addButton)
			self.left_layout.addWidget(self.left_deleteButton)
			self.left_layout.addWidget(self.left_list)
			QObject.connect(self.left_addButton,SIGNAL("released()"),self._addLeft)
			QObject.connect(self.left_deleteButton,SIGNAL("released()"),self._deleteLeft)
			for k in self.entry.keyslist:
				self.left_list.addItem(k.value)
		
		def _addLeft(self):
			s=self.lineedit.text()
			if s:
				k=self.entry.addKey(unicode(s))
				if k:
					self.left_list.addItem(s)
					self.lineedit.clear()
		def _deleteLeft(self):
			l=self.left_list.selectedItems()
			if not l:
				return
			sel=l[0]
			if sel:
				self.entry.removeKey(unicode(sel.text()))
				self.left_list.takeItem(self.left_list.row(sel))
		def __initRightList(self):
			self.right_layout=QVBoxLayout()
			self.layout.addLayout(self.right_layout)
			self.right_addButton=QPushButton(_('add'))
			self.right_deleteButton=QPushButton(_('delete'))
			self.right_list=QListWidget()
			self.right_layout.addWidget(self.right_addButton)
			self.right_layout.addWidget(self.right_deleteButton)
			self.right_layout.addWidget(self.right_list)
			QObject.connect(self.right_addButton,SIGNAL("released()"),self._addRight)
			QObject.connect(self.right_deleteButton,SIGNAL("released()"),self._deleteRight)
			for v in self.entry.valueslist:
				self.right_list.addItem(v.value)
		def _addRight(self):
			s=self.lineedit.text()
			if s:
				v=self.entry.addValue(unicode(s))
				if v:
					self.right_list.addItem(s)
					self.lineedit.clear()
		def _deleteRight(self):
			l=self.right_list.selectedItems()
			if not l:
				return
			sel=l[0]
			if sel:
				self.entry.removeValue(unicode(sel.text()))
				self.right_list.takeItem(self.right_list.row(sel))
		def __initButtons(self):
			self.button_layout=QHBoxLayout()

			self.delete_button=QPushButton(_('delete'))
			self.signal_button=QPushButton(_('edit signal'))

			self.button_layout.addWidget(self.delete_button)
			self.button_layout.addWidget(self.signal_button)
			self.main_layout.addLayout(self.button_layout)

			QObject.connect(self.delete_button,SIGNAL("released()"),self._delete)
			QObject.connect(self.signal_button,SIGNAL("released()"),self._editSignal)

			self.signal_dialog=cr.gui.SignalDialog(self.unit.signal_system,self.entry.signal,self.entry.args,self.unit.hasargs,parent=self)

			if not self.unit.hassignal:
				self.signal_button.setEnabled(False)


		def _delete(self):
			self.close()
			self.unit.removeEntry(self.entry)
		def _editSignal(self):
			msger=self.signal_dialog.get()
			if msger.signal is not None:
				self.entry.signal=msger.signal
				self.args=msger.args


	class _UnitWidget(QGroupBox):
		def __init__(self,unit,database):
			super(DatabaseAdvancedEdit._UnitWidget,self).__init__()
			self.unit=unit
			self.database=database
			self.__initWindow()
		def __initWindow(self):
			self.layout=QHBoxLayout()
			
			self.button_layout=QGridLayout()
			self.button_layout.setSpacing(0)

			self.add_button=QPushButton(_('new entry'))
			self.button_layout.addWidget(self.add_button,0,0,1,3)
			QObject.connect(self.add_button,SIGNAL("released()"),self.__addNewEntry)

			self.teach_priority_spinbox=QSpinBox()
			self.teach_priority_spinbox.setValue(self.unit.teach_priority)
			QObject.connect(self.teach_priority_spinbox,SIGNAL("valueChanged(int)"),self.__set_teach_priority)
			self.teach_priority_label=QLabel(_('teach priority'))
			self.button_layout.addWidget(self.teach_priority_label,1,0,1,1)
			self.button_layout.addWidget(self.teach_priority_spinbox,1,1,1,2)

			self.call_priority_spinbox=QSpinBox()
			self.call_priority_spinbox.setValue(self.unit.call_priority)
			QObject.connect(self.call_priority_spinbox,SIGNAL("valueChanged(int)"),self.__set_call_priority)
			self.call_priority_label=QLabel(_('call priority'))
			self.button_layout.addWidget(self.call_priority_label,2,0,1,1)
			self.button_layout.addWidget(self.call_priority_spinbox,2,1,1,2)

			self.msger_args_mode_combobox_dialog=cr.gui.ComboBoxDialog('select messager args mode',ARGS_MODE_FLAGS.values(),self.unit.msger_args_mode,parent=self)
			self.msger_args_mode_button=QPushButton(_('messager args mode:%s',_(self.unit.msger_args_mode)))
			QObject.connect(self.msger_args_mode_button,SIGNAL("released()"),self.__set_msger_args_mode_by_dialog)
			self.button_layout.addWidget(self.msger_args_mode_button,3,0,1,3)

			self.msger_kwargs_name_edit=QLineEdit()
			self.msger_kwargs_name_edit.setText(self.unit.msger_kwarg_name)
			self.msger_kwarg_name_label=QLabel(_('kwarg name'))
			self.button_layout.addWidget(self.msger_kwarg_name_label,4,0,1,1)
			self.button_layout.addWidget(self.msger_kwargs_name_edit,4,1,1,2)
			if self.unit.msger_args_mode!=ARGS_MODE_FLAGS.KEYWORD:
				self.msger_kwargs_name_edit.setEnabled(False)
			QObject.connect(self.msger_kwargs_name_edit,SIGNAL("textChanged(QString)"),self.__set_msger_kwargs_name_by_edit)

			self.layout.addLayout(self.button_layout)
			self.setTitle(self.unit.id)
			self.setLayout(self.layout)

			if not self.unit.hassignal:
				self.call_priority_spinbox.setEnabled(False)
				self.msger_args_mode_button.setEnabled(False)
				self.msger_kwargs_name_edit.setEnabled(False)
			for e in self.unit.entrieslist:
				self.addEntry(e)
		def __set_call_priority(self):
			self.unit.call_priority=self.call_priority_spinbox.value()
		def __set_teach_priority(self):
			self.unit.teach_priority=self.teach_priority_spinbox.value()
		def __set_msger_args_mode_by_dialog(self):
			self.unit.msger_args_mode=self.msger_args_mode_combobox_dialog.get()
			self.msger_args_mode_button.setText(_('messager args mode:%s',_(self.unit.msger_args_mode)))
			if self.unit.msger_args_mode==ARGS_MODE_FLAGS.KEYWORD:
				self.msger_kwargs_name_edit.setEnabled(True)
			else:
				self.msger_kwargs_name_edit.setEnabled(False)
		def __set_msger_kwargs_name_by_edit(self):
			self.unit.msger_kwarg_name=unicode(self.msger_kwargs_name_edit.text())
		def __addNewEntry(self):
			entry=self.database.getEntry(True)
			self.unit.addEntry(entry)
			self.addEntry(entry)
		def addEntry(self,entry):
			self.layout.addWidget(DatabaseAdvancedEdit._EntryWidget(entry,self.unit))
	def __init__(self,database,parent=None):
		super(DatabaseAdvancedEdit,self).__init__(parent)
		cr.core.crtry.checktype('database',database,cr.core.Database)
		self.setWindowTitle(_('setting'))
		self.unitsnumber=0
		
		self._initWindow()
		self.database=database
		self._initDatabase()
	def _initDatabase(self):
		for u in self.database.notReadonlyUnits():
			self.addUnit(u)
	def _initWindow(self):
		self.widget=QWidget()
		self.scrollarea=QScrollArea()
		self.setCentralWidget(self.scrollarea)
		self.scrollarea.setWidgetResizable(True)
		self.scrollarea.setWidget(self.widget)
		self.item_layout=QHBoxLayout(self.widget)
	def addUnit(self,unit):
		item=self._UnitWidget(unit,self.database)
		self.item_layout.addWidget(item)



class DatabaseAdvancedSetting(QDialog):
	def __init__(self,database,parent=None):
		super(DatabaseAdvancedSetting,self).__init__(parent)
		self.layout=QVBoxLayout(self)
		self.database=database
		self.setting_widget=DatabaseAdvancedEdit(database)
		self._initTop()
		self.layout.addWidget(self.setting_widget)
	def _initTop(self):
		self.top_layout=QHBoxLayout()
		self.layout.addLayout(self.top_layout)
		self.save_button=QPushButton(_('save'))
		self.top_layout.addWidget(self.save_button)
		QObject.connect(self.save_button,SIGNAL("released()"),self.database.save)




class DatabaseEdit(QDialog):
	def __init__(self,database,parent=None):
		super(DatabaseEdit,self).__init__(parent)
		self.database=database
		self._initWindow()
		self.advanced=None
		self.units_manager=AppManager(self.database)
		self.units_manager.setWindowTitle(_('Databse Units Manager'))
	def _initWindow(self):
		self.layout=QVBoxLayout(self)
		self.key_edit=QLineEdit()
		self.synonym_edit=QLineEdit()
		self.reply_edit=QLineEdit()
		self.add_button=QPushButton(_('add'))
		self.del_button=QPushButton(_('delete'))
		self.manage_units_button=QPushButton(_('manage units'))
		self.advanced_button=QPushButton(_('advanced setting'))
		self.save_button=QPushButton(_('save'))
		
		QObject.connect(self.add_button,SIGNAL("released()"),self._add)
		QObject.connect(self.del_button,SIGNAL("released()"),self._remove)
		QObject.connect(self.manage_units_button,SIGNAL("released()"),self._manage_units)
		QObject.connect(self.save_button,SIGNAL("released()"),self._save)
		QObject.connect(self.advanced_button,SIGNAL("released()"),self._showAdvancedSetting)

		key_layout=QHBoxLayout()
		key_layout.addWidget(QLabel(_('key')))
		key_layout.addWidget(self.key_edit)
		self.layout.addLayout(key_layout)

		synonym_layout=QHBoxLayout()
		synonym_layout.addWidget(QLabel(_('synonym')))
		synonym_layout.addWidget(self.synonym_edit)
		self.layout.addLayout(synonym_layout)

		reply_layout=QHBoxLayout()
		reply_layout.addWidget(QLabel(_('reply')))
		reply_layout.addWidget(self.reply_edit)
		self.layout.addLayout(reply_layout)

		b_layout_e=QHBoxLayout()
		b_layout_e.addWidget(self.add_button)
		b_layout_e.addWidget(self.del_button)
		self.layout.addLayout(b_layout_e)

		b_layout_s=QHBoxLayout()
		b_layout_s.addWidget(self.manage_units_button)
		b_layout_s.addWidget(self.advanced_button)
		self.layout.addLayout(b_layout_s)


		self.layout.addWidget(self.save_button)

	def _add(self):
		ks=unicode(self.key_edit.text())
		ss=unicode(self.synonym_edit.text())
		rs=unicode(self.reply_edit.text())
		if ks:
			self.key_edit.clear()
			if ss:
				self.database.addKey(ks,ss)
				self.synonym_edit.clear()
			if rs:
				self.database.addValue(ks,rs)
				self.reply_edit.clear()	
	def _remove(self):
		ks=unicode(self.key_edit.text())
		ss=unicode(self.synonym_edit.text())
		rs=unicode(self.reply_edit.text())
		if ks:
			self.database.removeKey(ks)
			self.key_edit.clear()
		if rs:
			self.database.removeValue(rs)
			self.reply_edit.clear()
	def _save(self):
		self.database.save()
	def _manage_units(self):
		self.units_manager.show()
	def _showAdvancedSetting(self):
		if self.advanced:
			self.advanced.close()
		self.advanced=DatabaseAdvancedSetting(self.database,parent=self)
		self.advanced.setWindowTitle(self.windowTitle())
		self.advanced.show()
	def show(self,key=None):
		if key is not None:
			self.key_edit.setText(key)
		super(DatabaseEdit,self).show()