#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:15:18 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from feriadosDialog_ui import Ui_FeriadosDialog
from modificarFeriadosDialog_ui import Ui_ModificarFeriadosDialog
from database_test import getIDCurrentPeriod,getFeriados,addFeriados,deleteFeriados
import datetime

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
    
class feriadosDialog(QtWidgets.QDialog):
    def __init__(self,conn,userID,parent):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_FeriadosDialog()
        self.ui.setupUi(self)
        self.setFixedSize(362,280)
        self.connection = conn
        self.userID = userID
        self.parent = parent
        self.showFeriados()
        return
    
    def showFeriados(self):
        IDCurrentPeriod = getIDCurrentPeriod(self.connection)
        Feriados = getFeriados(self.connection,IDCurrentPeriod)
        self.ui.table_feriados.clearContents()
        self.ui.table_feriados.setRowCount(0)
        for iFeriados in Feriados:
            currentRow = self.ui.table_feriados.rowCount()
            self.ui.table_feriados.setRowCount(currentRow+1)
            it0 = QtWidgets.QTableWidgetItem(str(iFeriados[0]))
            it0.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_feriados.setItem(currentRow,0,it0)
            it1 = QtWidgets.QTableWidgetItem(str(iFeriados[1]))
            it1.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_feriados.setItem(currentRow,1,it1)
            
    def agregarFeriados(self):
        dialog = QtWidgets.QDialog()
        dialog.setFixedSize(190,145)
        mfDialog=Ui_ModificarFeriadosDialog()
        mfDialog.setupUi(dialog)
        mfDialog.fecha_feriado.setDate(datetime.datetime.now())
        Result = dialog.exec_()
        
        if Result:
            Fecha = mfDialog.fecha_feriado.date()
            Razon = mfDialog.razon_feriado.toPlainText()
            Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea agregar el día '+str(Fecha.toString('dd/MM/yyyy'))+' como feriado ?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if Rta==QtWidgets.QMessageBox.Yes:
                IDCurrentPeriod = getIDCurrentPeriod(self.connection)
                Result = addFeriados(self.connection,IDCurrentPeriod,Fecha,Razon)
                if Result==0:
                    QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
                    self.showFeriados()
                    self.parent.colourFeriados()
                elif Result==23505:
                    QtWidgets.QMessageBox.critical(self,'Error '+str(Result),'Usted ya seleccionó este día como feriado')
                else:
                    QtWidgets.QMessageBox.critical(self,'Error '+str(Result),'No se pudo realizar la operación solicitada')
            else:
                QtWidgets.QMessageBox.information(self,'Cancelada','Solicitud cancelada')
        
        return

        
    def eliminarFeriados(self):
        dialog = QtWidgets.QDialog()
        dialog.setFixedSize(190,145)
        mfDialog=Ui_ModificarFeriadosDialog()
        mfDialog.setupUi(dialog)
        mfDialog.fecha_feriado.setDate(datetime.datetime.now())
        mfDialog.razon_feriado.setEnabled(False)
        Result = dialog.exec_()
        
        if Result:
            Fecha = mfDialog.fecha_feriado.date()
            Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea eliminar el día '+str(Fecha.toString('dd/MM/yyyy'))+' como feriado ?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if Rta==QtWidgets.QMessageBox.Yes:
                IDCurrentPeriod = getIDCurrentPeriod(self.connection)
                Result = deleteFeriados(self.connection,IDCurrentPeriod,Fecha)
                if Result==1:
                    QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
                elif Result==0:
                    QtWidgets.QMessageBox.critical(self,'Error','No existe ningún feriado en esa fecha')
                else:
                    QtWidgets.QMessageBox.critical(self,'Error '+str(Result),'No se pudo realizar la operación solicitada')
                self.showFeriados()
                self.parent.colourFeriados()
            else:
                QtWidgets.QMessageBox.information(self,'Cancelada','Solicitud cancelada')