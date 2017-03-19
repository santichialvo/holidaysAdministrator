# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:02:54 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from notificationsWidget_ui import Ui_NotificationsWidget
from database_test import getIDCurrentPeriod,searchAllNotifications

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
    
class notificationsWidget(QtWidgets.QWidget):
    def __init__(self,conn,userID):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_NotificationsWidget()
        self.ui.setupUi(self)
        self.connection = conn
        self.currentUserID = userID
        self.showAllNotifications()
        return
    
    def showAllNotifications(self):
        self.ui.notifications_tableWidget.clearContents()
        self.ui.notifications_tableWidget.setRowCount(0)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        AllNotifications=searchAllNotifications(self.connection,IDCurrentPeriod)
        for iNotification in AllNotifications:
            currentRow=self.ui.notifications_tableWidget.rowCount()
            self.ui.notifications_tableWidget.setRowCount(currentRow+1)
            it0=QtWidgets.QTableWidgetItem(str(iNotification[0]))
            it0.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.notifications_tableWidget.setItem(currentRow,0,it0)
            it1=QtWidgets.QTableWidgetItem(str(iNotification[1]))
            it1.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.notifications_tableWidget.setItem(currentRow,1,it1)
        return