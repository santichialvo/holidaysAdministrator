# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 20:41:20 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from employeeWindow import employeeWindow
from utils import showMessage
import sys, os
import qdarkstyle

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
    # create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    os.environ["HM_INST_DIR"] = "C:\\Users\\Santiago\\Desktop\\holidaysAdministrator"
    
    ew = employeeWindow()
    result = ew.login()
    while not result:
        showMessage('Usuario o contraseña inválido. Por favor, intentelo de nuevo')
        result = ew.login()
    if result<0:
        sys.exit(0)
    ew.show()
    ew.loadData()
    sys.exit(app.exec_())
    return
 
if __name__ == '__main__':
    main()
