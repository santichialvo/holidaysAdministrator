# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 20:41:20 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from employeeWindow import employeeWindow
import sys

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

def main():
    app = QtWidgets.QApplication(sys.argv)
    ew = employeeWindow()
    result = ew.login()
    while not result:
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,'Error','Usuario o contraseña inválido. Por favor, intentelo de nuevo').exec_()
        result = ew.login()
    if result<0:
        sys.exit(0)
    ew.show()
    ew.loadData()
    sys.exit(app.exec_())
    return
 
if __name__ == '__main__':
    main()