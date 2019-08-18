# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:57:58 2019

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from changePasswordDialog_ui import Ui_ChangePasswordDialog

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

class changePasswordDialog(QtWidgets.QDialog):
    def __init__(self, connection):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_ChangePasswordDialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.setBaseSize(230, 20)
        return