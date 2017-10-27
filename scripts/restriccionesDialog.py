#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 13:05:53 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from restriccionesDialog_ui import Ui_RestriccionesDialog
from database_test import getRestricciones,searchNameForUserByID

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
        