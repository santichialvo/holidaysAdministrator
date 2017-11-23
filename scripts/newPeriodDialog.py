#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:09:21 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from newPeriodDialog_ui import Ui_NewPeriodDialog
from database_test import getPeriodos,deletePeriodByYear,getIDCurrentPeriod,getAnioPeriod

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
class newPeriodDialog(QtWidgets.QDialog):
    def __init__(self,conn,userID):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_NewPeriodDialog()
        self.ui.setupUi(self)
        self.setFixedSize(230,180)
        self.connection = conn
        self.currentUserID = userID
        self.showPeriods()
        return
    
    def showPeriods(self):
        Periodos = getPeriodos(self.connection)
        for iPeriodos in Periodos:
            self.ui.period_listWidget.addItem(str(iPeriodos[0]))
        return
    
    def deletePeriod(self):
        Item = self.ui.period_listWidget.currentItem()
        if not Item:
            QtWidgets.QMessageBox.critical(self,'Error','Debe seleccionar un periodo')
            return
        ItemText = Item.text()
        Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea eliminar el periodo '+str(ItemText)+'? Considere que todas las solicitudes y notificaciones serán también eliminadas',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if Rta==QtWidgets.QMessageBox.Yes: 
            currentPeriod = getIDCurrentPeriod(self.connection)
            Anio=getAnioPeriod(self.connection,currentPeriod)
            if (Anio==ItemText):
                QtWidgets.QMessageBox.critical(self,'Error','No puede eliminar el periodo actual')
            rows=deletePeriodByYear(self.connection,ItemText)
            if (rows==1):
                QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
            else:
                QtWidgets.QMessageBox.critical(self,'Error '+str(rows),'El periodo no pudo ser eliminado')
        return
    
    def selectPeriod(self,item):
        Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea utilizar el periodo '+str(item.text())+' como activo?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        return
                
        
        
        