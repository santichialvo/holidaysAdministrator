# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:39:12 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from loginWindow_ui import Ui_LoginWindow
from database_test import searchForUsers

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
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        return
        
    def checkUser(self,conn):
        Usuario=str(self.ui.Usuario.text())
        Password=str(self.ui.Password.text())
        Matches=searchForUsers(Usuario,Password,conn)
        return Matches
        
        
        