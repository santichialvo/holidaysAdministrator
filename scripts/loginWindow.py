# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:39:12 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from loginWindow_ui import Ui_LoginWindow
from changePasswordDialog import changePasswordDialog
from database_test import searchForUsers, searchUserByLogin, changePassword
from utils import showMessage

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

class loginWindow(QtWidgets.QDialog):
    def __init__(self, connection):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.connection = connection
        self.setBaseSize(383, 126)
        return

    def checkUser(self):
        Usuario = str(self.ui.Usuario.text())
        Password = str(self.ui.Password.text())
        Matches = searchForUsers(Usuario, Password, self.connection)
        return Matches

    def changePassword(self):
        Usuario = str(self.ui.Usuario.text())
        Matches = searchUserByLogin(Usuario, self.connection)
        if not Matches:
            showMessage("Por favor, ingrese un usuario valido")
            return
        cpd = changePasswordDialog(self.connection)
        result = cpd.exec_()
        if result:
            Password = str(cpd.ui.oldPasswordLineEdit.text())
            Matches = searchForUsers(Usuario, Password, self.connection)
            if not Matches:
                showMessage("La contraseña actual no es correcta")
                return
            newPassword = str(cpd.ui.newPasswordLineEdit.text())
            newPassword2 = str(cpd.ui.repeatNewPasswordLineEdit.text())
            if newPassword != newPassword2:
                showMessage("La contraseñas nuevas no coinciden")
                return
            msg = "¿Está seguro de cambiar su contraseña?" 
            reply = showMessage(msg, 4, QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                ret = changePassword(Usuario, newPassword, self.connection)
                if not ret:
                    showMessage("Operación exitosa", 1)
                else:
                    showMessage("Operación cancelada", 1)
                    return
            
            
        return
        
        
        