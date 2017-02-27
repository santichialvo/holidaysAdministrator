# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:39:12 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2,datetime,sys
from employeeWindow_ui import Ui_EmployeeWindow
from loginWindow import loginWindow
from dayRequestWindow import dayRequestWindow
from cancelRequestWindow import cancelRequestWindow
from database_test import searchUserByID,searchDaysAcceptedByID,searchRequestsByUserID

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
    
class employeeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_EmployeeWindow()
        self.ui.setupUi(self)
        self.setFixedSize(910,370)
        
        try:
            self.connection = psycopg2.connect("dbname='HolidaysAdministrator' user='postgres' host='localhost' password=''")
        except:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,'Error','Fallo en la conexión con la base de datos. Compruebe que la máquina servidor este encendida').exec_()
            sys.exit(1)
        
        self.currentUserID = 1
        return
    
    def login(self):
        lw = loginWindow()
        result = lw.exec_()
        if result:
            Matches = lw.checkUser(self.connection)
            self.currentUserID = Matches[0][0] if len(Matches)>0 else -1
            return len(Matches)
        else:
            return -1
    
    def loadData(self):
        if (self.currentUserID<0):
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,'Error','Ha ocurrido un error. Por favor comuníquese con el administrador').exec_()
            sys.exit(1)
        
        UserTuple = searchUserByID(self.currentUserID,self.connection)
        if (len(UserTuple)>1):
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,'Error','Ha ocurrido un error. Por favor comuníquese con el administrador').exec_()
            sys.exit(1)
            
        self.currentUserName = UserTuple[0][1]
        self.currentUserMail = UserTuple[0][5]
        self.ui.label_presentacion.setText('Hola, %s'%self.currentUserName)
        
        self.colourRequestedDays()
        self.showRequests()
        return
        
    def showRequests(self):
        Requests = searchRequestsByUserID(self.currentUserID,self.connection)
        self.ui.table_solicitudes.clearContents()
        self.ui.table_solicitudes.setRowCount(0)
        for irequest in Requests:
            currentRow=self.ui.table_solicitudes.rowCount()
            self.ui.table_solicitudes.setRowCount(currentRow+1)
            it0=QtWidgets.QTableWidgetItem(str(irequest[0]))
            it0.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,0,it0)
            it1=QtWidgets.QTableWidgetItem(str(irequest[1].day)+'/'+str(irequest[1].month)+'/'+str(irequest[1].year))
            it1.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,1,it1)
            it2=QtWidgets.QTableWidgetItem(str(irequest[2].day)+'/'+str(irequest[2].month)+'/'+str(irequest[2].year) if irequest[2] is not None else '-')
            it2.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,2,it2)
            it3=QtWidgets.QTableWidgetItem(str('Día completo') if irequest[3]==0 else str('Medio día (mañana)') if irequest[3]==1 else str('Medio día (tarde)') if irequest[3]==2 else str('-'))
            it3.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,3,it3)
            it4=QtWidgets.QTableWidgetItem(str('Pendiente') if irequest[4]=='P' else str('Aprobada') if irequest[4]=='A' else str('Rechazada'))
            it4.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,4,it4)
        return
        
        
    def colourRequestedDays(self):
        format_reqday_complete = QtGui.QTextCharFormat()
        format_reqday_complete.setBackground(QtCore.Qt.yellow)
        format_reqday_half = QtGui.QTextCharFormat()
        format_reqday_half.setBackground(QtCore.Qt.green)
        Days = searchDaysAcceptedByID(self.currentUserID,self.connection)
        for iday in Days:
            if iday[1]!=None:
                currDay=iday[0]
                maxDay=iday[1]
                while currDay<=maxDay:
                    day = QtCore.QDate(currDay.year,currDay.month,currDay.day)
                    self.ui.calendario.setDateTextFormat(day,format_reqday_complete)
                    currDay += datetime.timedelta(1)
            else:
                day = QtCore.QDate(iday[0].year,iday[0].month,iday[0].day)
                self.ui.calendario.setDateTextFormat(day,format_reqday_complete if iday[2] is None else format_reqday_half)
                
    def requestDay(self):
        drw = dayRequestWindow()
        result = drw.exec_()
        if result:
            Return=drw.requestDays(self.currentUserID,self.connection)
            if (Return==0):
                self.showRequests()

    def cancelRequest(self):
        crw = cancelRequestWindow()
        result = crw.exec_()
        if result:
            Return=crw.searchAndDeleteRequest(self.currentUserID,self.connection)
            if Return==0:
                self.showRequests()
        return