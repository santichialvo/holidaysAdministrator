# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:11:40 2017

@author: Santiago
"""

from PyQt5 import QtWidgets
from addRemoveEmployeeDialog_ui import Ui_AddRemoveEmployeeDialog
from addEmployeeDialog_ui import Ui_AddEmployeeDialog
from database_test import searchAllUsersID,searchNameForUserByID,deleteEmployee, \
                          getUserID,createRol,addEmployee,getAllPeriods,setDaysForNewUser
from utils import showMessage
    
class addRemoveEmployeeDialog(QtWidgets.QDialog):
    def __init__(self,conn,userID,parent):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_AddRemoveEmployeeDialog()
        self.ui.setupUi(self)
        self.connection = conn
        self.currentUserID = userID
        self.parent = parent
        self.setFixedSize(320,82)
        self.fillComboBox()
        return
    
    def fillComboBox(self):
        self.ui.employee_comboBox.clear()
        AllUsersIDs=searchAllUsersID(self.connection)
        for UserID in AllUsersIDs:
            Nombre=searchNameForUserByID(self.connection,UserID[0])
            self.ui.employee_comboBox.addItem(Nombre[0][0]+' '+Nombre[0][1])
        return
    
    def addEmployee(self):
        dialog = QtWidgets.QDialog()
        dialog.setFixedSize(335,225)
        addDialog=Ui_AddEmployeeDialog()
        addDialog.setupUi(dialog)
        Res = dialog.exec_()
        if Res:
            nombre = str(addDialog.nombre.text())
            apellido = str(addDialog.apellido.text())
            usuario = str(addDialog.usuario.text())
            password = str(addDialog.password.text())
            email = str(addDialog.email.text())
            rol = str(addDialog.rol.currentText())
            msg = '¿Desea incorporar a '+nombre+' '+apellido+' al sistema?'
            Rta = showMessage(msg, 4, QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            if (Rta==QtWidgets.QMessageBox.Yes):
                Res=addEmployee(self.connection,nombre,apellido,usuario,password,email)
                if (Res==0):
                    UserID = getUserID(self.connection,nombre,apellido)
                    Res = createRol(self.connection,UserID,rol)
                    if (Res!=0):
                        showMessage('Error creando los roles para el nuevo usuario. Contacte al administrador inmediatamente.')
                        return
                    Periods=getAllPeriods(self.connection)
                    for iPeriod in Periods:
                        # se crean tablas para todos los periodos existentes. Habría que cambiar esto
                        Res = setDaysForNewUser(self.connection,UserID,iPeriod[0])
                        if (Res!=0):
                            showMessage('Error creando los dias para el nuevo usuario. Contacte al administrador inmediatamente.')
                            return
                    self.parent.resetCalendar()
                    self.parent.showEmployeeStatus()
                    self.parent.colourRequestedDays()
                    self.parent.colourFeriados()
                    self.fillComboBox()
                    QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
                else:
                    showMessage('No se pudo realizar la operación solicitada')
            else:
                QtWidgets.QMessageBox.information(self,'Cancelada','Operación cancelada')
        return
    
    def removeEmployee(self):
        employeeStr = str(self.ui.employee_comboBox.currentText())
        employee = employeeStr.split(' ')
        UserID = getUserID(self.connection,employee[0],employee[1])
        msg = '¿Desea eliminar al usuario '+employeeStr+' del sistema?'
        Rta = showMessage(msg, 4, QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if (Rta==QtWidgets.QMessageBox.Yes):
            # reseteo antes de eliminarlo
            self.parent.resetCalendar()
            Ret = deleteEmployee(self.connection,UserID)
            if (Ret==1):
                self.parent.showEmployeeStatus()
                self.parent.colourRequestedDays()
                self.parent.colourFeriados()
                self.fillComboBox()
                QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
            else:
                showMessage('No se pudo realizar la operación solicitada')
        else:
            QtWidgets.QMessageBox.information(self,'Cancelada','Operación cancelada')
        return