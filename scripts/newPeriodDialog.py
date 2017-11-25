#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:09:21 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from newPeriodDialog_ui import Ui_NewPeriodDialog
from database_test import getPeriodos,deletePeriodByYear,getIDCurrentPeriod,getAnioPeriod,activate_deactivatePeriod
from utils import my_assert

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
    def __init__(self,conn,userID,parent):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_NewPeriodDialog()
        self.ui.setupUi(self)
        self.setFixedSize(230,180)
        self.connection = conn
        self.currentUserID = userID
        self.parent = parent
        self.showPeriods()
        return
    
    def showPeriods(self):
        Periodos = getPeriodos(self.connection)
        for iPeriodos in Periodos:
            self.ui.period_listWidget.addItem(str(iPeriodos[0]))
        self.setActive()
        return
    
    def setActive(self,oldYear=None):
        currentPeriod = getIDCurrentPeriod(self.connection)
        Anio=getAnioPeriod(self.connection,currentPeriod)
        item=self.ui.period_listWidget.findItems(str(Anio),QtCore.Qt.MatchExactly)
        my_assert(self,len(item)==1,'El periodo actual sólo puede ser uno. Contacte al administrador.')
        item[0].setFlags(item[0].flags() ^ QtCore.Qt.ItemIsEnabled)
#        item[0].setFlags(item[0].flags() ^ QtCore.Qt.ItemIsSelectable)
        if oldYear:
            item=self.ui.period_listWidget.findItems(str(oldYear),QtCore.Qt.MatchExactly)
            my_assert(self,len(item)==1,'El periodo a desactivar sólo puede ser uno. Contacte al administrador.')
            item[0].setFlags(QtCore.Qt.ItemIsEnabled)
#            item[0].setFlags(QtCore.Qt.ItemIsSelectable)
        return
    
    def deletePeriod(self):
        Item = self.ui.period_listWidget.currentItem()
        if not Item:
            QtWidgets.QMessageBox.critical(self,'Error','Debe seleccionar un periodo')
            return
        ItemText = Item.text()
        currentPeriod = getIDCurrentPeriod(self.connection)
        Anio = getAnioPeriod(self.connection,currentPeriod)
        if (ItemText==str(Anio)):
            QtWidgets.QMessageBox.critical(self,'Error','El periodo a eliminar no puede ser el actual')
            return
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
    
    def addPeriod(self):
        
        return
    
    def selectPeriod(self,item):
        newAnio=str(item.text())
        Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea utilizar el periodo '+newAnio+' como activo?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if Rta==QtWidgets.QMessageBox.Yes:
            currentPeriod = getIDCurrentPeriod(self.connection)
            # reseteo calendario antes de que se cambie el periodo activo
            self.parent.resetCalendar()
            Anio=getAnioPeriod(self.connection,currentPeriod)
            Ret=activate_deactivatePeriod(self.connection,Anio,False)
            if (Ret!=0):
                QtWidgets.QMessageBox.critical(self,'Error '+Ret,'La operación no pudo realizarse')
                return
            Ret=activate_deactivatePeriod(self.connection,newAnio,True)
            if (Ret!=0):
                QtWidgets.QMessageBox.critical(self,'Error '+Ret,'La operación no pudo realizarse')
                return
            
            # cambio de periodo activo (en la ventana)
            self.setActive(Anio)
            # vuelvo a cargar las nuevas variables
            self.parent.showEmployeeStatus()
            self.parent.colourRequestedDays()
            self.parent.colourFeriados()
            
            QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
        return
                
        
        
        