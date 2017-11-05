#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 13:05:53 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from restriccionesDialog_ui import Ui_RestriccionesDialog
from addRestrictionDialog import addRestrictionDialog
from database_test import getRestricciones,searchNameForUserByID,searchAllUsersID, \
                            getUserID,addRestriccionesUsuarios,deleteRestriccionesUsuarios

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
    
class restriccionesDialog(QtWidgets.QDialog):
    def __init__(self,conn,userID):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_RestriccionesDialog()
        self.ui.setupUi(self)
        self.setFixedSize(400,300)
        self.connection = conn
        self.currentUserID = userID
        self.showRestricciones()
        return
    
    
    def showRestricciones(self):
        self.ui.restricciones_tableWidget.clearContents()
        self.ui.restricciones_tableWidget.setRowCount(0)
        Restricciones=getRestricciones(self.connection)
        for iRestricciones in Restricciones:
            iRestricciones=iRestricciones[0]
            text=''
            for iUsuario in iRestricciones:
                Usuario=searchNameForUserByID(self.connection,iUsuario)
                text+=(Usuario[0][0]+' '+Usuario[0][1]+' - ')
            text = text[0:-3] if text!='' else text
            currentRow=self.ui.restricciones_tableWidget.rowCount()
            self.ui.restricciones_tableWidget.setRowCount(currentRow+1)
            it0=QtWidgets.QTableWidgetItem(text)
            it0.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.restricciones_tableWidget.setItem(currentRow,0,it0)
        return
    
    def addRestriction(self):
        addrDialog = addRestrictionDialog(self.connection,self.currentUserID)
        Return=addrDialog.exec_()
        if Return:
            cantEmpleados = addrDialog.ui.employee_listWidget.count()
            if cantEmpleados==0:
                QtWidgets.QMessageBox.critical(self,'Error','No ha seleccionado ningún empleado')
            text = ''
            for iItem in xrange(cantEmpleados):
                item=addrDialog.ui.employee_listWidget.item(iItem)
                text = text + item.text() + ', '
            Ret=QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea agregar una restricción con '+str(text)+' a la lista?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if Ret==QtWidgets.QMessageBox.Yes:
                employeeList = '{'
                for iItem in xrange(cantEmpleados):
                    item=addrDialog.ui.employee_listWidget.item(iItem)
                    item=item.text().split(' ')
                    currID=getUserID(self.connection,item[0],item[1])
                    employeeList = employeeList + str(currID) + ','
                employeeList=employeeList[0:-1]
                employeeList=employeeList+'}'
                Ret = addRestriccionesUsuarios(self.connection,employeeList)
                if (Ret==0):
                    QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
                    self.showRestricciones()
                else:
                    QtWidgets.QMessageBox.critical(self,'Error','No se ha podido efectuar la operación')
        else:
            QtWidgets.QMessageBox.information(self,'Cancelada','Restricción cancelada')
            
    def deleteRestriction(self):
        employeeNames = self.ui.restricciones_tableWidget.currentItem().text()
        Ret=QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea eliminar la restricción de '+str(employeeNames)+' de la lista?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if (Ret==QtWidgets.QMessageBox.Yes):
            Names = employeeNames.split(' - ')
            employeeList = '{'
            for iNames in Names:
                iNames = iNames.split(' ')
                ID = getUserID(self.connection,iNames[0],iNames[1])
                employeeList = employeeList+str(ID)+','
            employeeList=employeeList[0:-1]
            employeeList=employeeList+'}'
            Rows = deleteRestriccionesUsuarios(self.connection,employeeList)
            if Rows!=0:
                QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
                self.showRestricciones()
            else:
                QtWidgets.QMessageBox.critical(self,'Error','No se ha podido efectuar la operación')
                
        return
                
            
        return
        