# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 17:34:08 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from dayRequestWindow_ui import Ui_DayRequestWindow
import datetime
from database_test import doRequestByID,searchRequestsByUserID,getIDCurrentPeriod

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
    
class dayRequestWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_DayRequestWindow()
        self.ui.setupUi(self)
        self.setFixedSize(362,280)
        self.ui.fechaDesde.setDate(datetime.datetime.now())
        self.ui.fechaHasta.setDate(datetime.datetime.now())
        self.maxLengthRazon = 120
        return
    
    def changeUniqueDay(self):
        if self.ui.diaUnico.isChecked():
            self.ui.fechaHasta.setEnabled(False)
            self.ui.diaUnicoComboBox.setEnabled(True)
        else:
            self.ui.fechaHasta.setEnabled(True)
            self.ui.diaUnicoComboBox.setEnabled(False)
            
    def requestDays(self,userID,conn):
        IDCurrentPeriod = getIDCurrentPeriod(conn)
        fechaDesde = self.ui.fechaDesde.date()
        fechaHasta = self.ui.fechaHasta.date() if self.ui.fechaHasta.isEnabled() else None
        Razon = self.ui.razon.toPlainText() if self.ui.razon.toPlainText()!='' else None
        MedioDia = self.ui.diaUnicoComboBox.currentIndex() if self.ui.diaUnico.isChecked() else None
        Tipo = self.ui.tipo.currentIndex()
                                         
        Requests=searchRequestsByUserID(userID,conn)
        for irequest in Requests:
            ReqFechaDesde = datetime.date(irequest[1].year,irequest[1].month,irequest[1].day)
            ReqFechaHasta = datetime.date(irequest[2].year,irequest[2].month,irequest[2].day) if irequest[2] is not None else None
            currFechaDesde = datetime.date(fechaDesde.year(),fechaDesde.month(),fechaDesde.day())
            currFechaHasta = datetime.date(fechaHasta.year(),fechaHasta.month(),fechaHasta.day()) if fechaHasta is not None else None
            if ReqFechaHasta:
                if ReqFechaDesde <= currFechaDesde <= ReqFechaHasta:
                    QtWidgets.QMessageBox.critical(self,'Error','Usted ya ha pedido ese día o alguno de esos días anteriormente. Por favor cancele la solicitud para volver a efectuarla')
                    return -1
            if currFechaHasta:
                if currFechaDesde <= ReqFechaDesde <= currFechaHasta:
                    QtWidgets.QMessageBox.critical(self,'Error','Usted ya ha pedido ese día o alguno de esos días anteriormente. Por favor cancele la solicitud para volver a efectuarla')
                    return -1
            if ReqFechaDesde==currFechaDesde:
                    QtWidgets.QMessageBox.critical(self,'Error','Usted ya ha pedido ese día o alguno de esos días anteriormente. Por favor cancele la solicitud para volver a efectuarla')
                    return -1
        
        QuestionStr = '¿Está seguro que desea solicitar los días %s a %s?'%(fechaDesde.toString('dd/MM/yyyy'),fechaHasta.toString('dd/MM/yyyy')) if fechaHasta is not None else '¿Está seguro que desea solicitar el día %s?'%fechaDesde.toString('dd/MM/yyyy')
        Rta = QtWidgets.QMessageBox.question(self,'Confirmación',QuestionStr,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if Rta==QtWidgets.QMessageBox.Yes:
            Return = doRequestByID(userID,conn,self.ui.fechaDesde.date(),Tipo,IDCurrentPeriod,fechaHasta,Razon,MedioDia)
            if Return==23505:   #unique violation
                QtWidgets.QMessageBox.critical(self,'Error','Usted ya ha pedido ese día o alguno de esos días anteriormente. Por favor cancele la solicitud para volver a efectuarla')
            elif Return==23514: #check violation
                QtWidgets.QMessageBox.critical(self,'Error','La fecha hasta debe ser mayor a la fecha desde')
            elif Return==0:     #exito
                QtWidgets.QMessageBox.information(self,'Exito','Solicitud enviada correctamente')
            return Return
        else:
            QtWidgets.QMessageBox.information(self,'Cancelada','Solicitud cancelada')
            return -1
    
    def controlLength(self):
        if len(self.ui.razon.toPlainText())>self.maxLengthRazon:
            self.ui.razon.setPlainText(self.ui.razon.toPlainText()[0:self.maxLengthRazon])