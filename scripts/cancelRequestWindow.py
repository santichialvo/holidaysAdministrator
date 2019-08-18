# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 08:20:19 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from cancelRequestWindow_ui import Ui_CancelRequestWindow
from database_test import searchRequestByIDs,deleteRequestByID
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
    
class cancelRequestWindow(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_CancelRequestWindow()
        self.ui.setupUi(self)
        self.setFixedSize(300,90)
        return
    
    def searchAndDeleteRequest(self,UserID,conn):
        ReqID = self.ui.spinBox_request.value()
        rows=searchRequestByIDs(ReqID,UserID,conn)
        if len(rows)==1:
            if rows[0][6]=='P':
                deleteRequestByID(ReqID,conn)
                QtWidgets.QMessageBox.information(self,'Exito','Solicitud cancelada')
                return 0
            else:
                showMessage('La solicitud ingresada ya fue aprobada o cancelada. Por favor contacte con el administrador')
                return -1    
        else:
            showMessage('La solicitud ingresada no existe')
            return -1
            