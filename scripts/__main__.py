# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 20:41:20 2017

@author: Santiago
"""

import os
import sys
import qdarkstyle
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from employeeWindow import employeeWindow
from utils import showMessage, INSTALLATION_FOLDER

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
    
    if not os.path.isdir(INSTALLATION_FOLDER):
        showMessage('No se puede ejecutar el programa. Ruta de instalación no encontrada')
        sys.exit(app.exec_())
        return
    
    # check for actualizations
#    updater_exe = os.path.join(INSTALLATION_FOLDER, "ADL Updater.exe")
#    process = subprocess.Popen([updater_exe])
#    process.wait()

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
