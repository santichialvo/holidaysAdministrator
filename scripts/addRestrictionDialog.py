#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 02:50:54 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from addRestrictionDialog_ui import Ui_addRestrictionDialog
from database_test import searchAllUsersID,searchNameForUserByID
    
class addRestrictionDialog(QtWidgets.QDialog):
    def __init__(self,conn,userID):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_addRestrictionDialog()
        self.ui.setupUi(self)
        self.connection = conn
        self.currentUserID = userID
        self.setFixedSize(275,150)
        
        self.addEmployeesToCB()
        self.currentEmployeesOnList = []
        return
    
    def addEmployeesToCB(self):
        AllUsersIDs=searchAllUsersID(self.connection)
        for UserID in AllUsersIDs:
            Nombre=searchNameForUserByID(self.connection,UserID[0])
            self.ui.employee_comboBox.addItem(Nombre[0][0]+' '+Nombre[0][1])
        return
        
    def addEmployeeToList(self):
        empleado = self.ui.employee_comboBox.currentText()
        Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea agregar a ' + str(empleado) + ' a la lista?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if Rta==QtWidgets.QMessageBox.Yes:
            if empleado in self.currentEmployeesOnList:
                QtWidgets.QMessageBox.critical(self,'Error','El empleado ya se encuentra en la lista')
            else:
                self.ui.employee_listWidget.addItem(empleado)
                self.currentEmployeesOnList.append(empleado)        
        return