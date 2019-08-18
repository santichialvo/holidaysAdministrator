# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:39:12 2017

@author: Santiago
"""

import psycopg2, datetime, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from utils import findIPfromMAC,calculateDays
from employeeWindow_ui import Ui_EmployeeWindow
from loginWindow import loginWindow
from dayRequestWindow import dayRequestWindow
from cancelRequestWindow import cancelRequestWindow
from requestsWidget import requestsWidget
from employeeWidget import employeeWidget
from notificationsWidget import notificationsWidget
from utils import showMessage, GREEN, YELLOW
from database_test import searchUserByID,searchDaysAcceptedByID,searchRequestsByUserID, \
                          getIDCurrentPeriod,searchNotificationsByID,getFeriados,searchDaysForUserByID, \
                          searchforAbsenceOrLicenseByUserID,getAnioPeriod

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
    
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
class employeeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_EmployeeWindow()
        self.ui.setupUi(self)
        self.setBaseSize(1150, 515)
        localTest = True

        if not localTest:
            IP = findIPfromMAC('00-1e-67-05-b5-49')
            # print(IP)
            if (IP.find('192.168')==-1):
                showMessage('Fallo en la detección de la IP. Compruebe que la máquina servidor este encendida')
                sys.exit(1)

        try:
            if localTest:
                self.connection = psycopg2.connect("dbname='holidaysAdministrator' user='postgres' host='localhost' password='comando09'")
            else:
                self.connection = psycopg2.connect("dbname='holidaysAdministrator' user='postgres' host='%s' password='comando09' port='5432'"%IP)
        except psycopg2.OperationalError as e:
            showMessage('Fallo en la conexión con la base de datos. Compruebe que la máquina servidor este encendida')
            sys.exit(1)

        self.currentUserID = 1
        return
    
    def login(self):
        lw = loginWindow(self.connection)
        result = lw.exec_()
        if result:
            Matches = lw.checkUser()
            self.currentUserID = Matches[0][0] if len(Matches)>0 else -1
            if Matches and len(Matches)!=2:
                self.ui.tab_admin.deleteLater()
            return len(Matches)
        else:
            return -1
    
    def loadData(self):
        if (self.currentUserID<0):
            showMessage('Ha ocurrido un error. Por favor comuníquese con el administrador')
            sys.exit(1)
        
        UserTuple = searchUserByID(self.currentUserID,self.connection)
        if (len(UserTuple)>1):
            showMessage('Ha ocurrido un error. Por favor comuníquese con el administrador')
            sys.exit(1)
            
        self.currentUserName = UserTuple[0][1]
        self.currentUserMail = UserTuple[0][5]
        
        self.changeView()
        return
    
    def setLabels(self):
        self.ui.label_presentacion.setText('Hola, %s'%self.currentUserName)
        # todo esto para calcular los días restantes.. -_-
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        Feriados=getFeriados(self.connection,IDCurrentPeriod)
        Dias=searchDaysForUserByID(self.connection,self.currentUserID,IDCurrentPeriod)
        DaysTotal=Dias[0][0]
        Absences=searchforAbsenceOrLicenseByUserID(self.connection,self.currentUserID,IDCurrentPeriod,True)
        DaysAbsences=calculateDays(Absences,Feriados)
        Licenses=searchforAbsenceOrLicenseByUserID(self.connection,self.currentUserID,IDCurrentPeriod,False)
        DaysLicenses=calculateDays(Licenses,Feriados)
        RestOfDays=DaysTotal-DaysAbsences-DaysLicenses
        self.ui.label_dias.setText('Días restantes: %s'%RestOfDays)
        Anio=getAnioPeriod(self.connection,IDCurrentPeriod)
        self.ui.label_periodo.setText('Período: %s'%Anio)
        return
    
    def changeView(self):
        self.setLabels()
        self.colourRequestedDays()
        self.showRequests()
        self.showNotifications()
        if self.ui.tab_admin:
            self.updateCaseSetup(self.ui.adminListWidget.currentItem())
        
    def showRequests(self):
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        Requests = searchRequestsByUserID(self.currentUserID,IDCurrentPeriod,self.connection,False)
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
            it4=QtWidgets.QTableWidgetItem(str('Licencia') if irequest[4]==0 else str('Ausencia'))
            it4.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,4,it4)
            it5=QtWidgets.QTableWidgetItem(str('Pendiente') if irequest[5]=='P' else str('Aprobada') if irequest[5]=='A' else str('Rechazada'))
            it5.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_solicitudes.setItem(currentRow,5,it5)
        return
    
    def showNotifications(self):
        self.ui.table_notificaciones.clearContents()
        self.ui.table_notificaciones.setRowCount(0)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        UserNotifications=searchNotificationsByID(self.connection,IDCurrentPeriod,self.currentUserID)
        for iNotification in UserNotifications:
            currentRow=self.ui.table_notificaciones.rowCount()
            self.ui.table_notificaciones.setRowCount(currentRow+1)
            it0=QtWidgets.QTableWidgetItem(str(iNotification[0]))
            it0.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_notificaciones.setItem(currentRow,0,it0)
            
            aux = 'descontado ' if iNotification[3]==0 else 'agregado '
            msj = 'Se le han ' + aux + str(iNotification[2]) + ' días por la razón: ' + str(iNotification[1])
            it1=QtWidgets.QTableWidgetItem(str(msj))
            it1.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.table_notificaciones.setItem(currentRow,1,it1)
        
    def colourRequestedDays(self):
        format_reqday_complete = QtGui.QTextCharFormat()
        format_reqday_complete.setBackground(YELLOW)
        format_reqday_half = QtGui.QTextCharFormat()
        format_reqday_half.setBackground(GREEN)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        Days = searchDaysAcceptedByID(self.currentUserID,self.connection,IDCurrentPeriod)
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
                self.ui.calendario.setDateTextFormat(day,format_reqday_complete if iday[2]==0 else format_reqday_half)
                
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
    
    def closeEvent(self, ev):
        msg = '¿Está seguro de que desea salir del Administrador de Licencias?'
        Rta = showMessage(msg, 4, QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if Rta == QtWidgets.QMessageBox.No:
            ev.ignore()
        return
    
    def updateCaseSetup(self, QListWidgetItem):
        if not QListWidgetItem:
            return
        
        menu=str(QListWidgetItem.text())
        if menu == 'Solicitudes':
            widget = requestsWidget(self.connection,self.currentUserID)
        elif menu == 'Empleados':
            widget = employeeWidget(self.connection,self.currentUserID)
        elif menu == 'Notificaciones':
            widget = notificationsWidget(self.connection,self.currentUserID)
        else:
            widget = requestsWidget(self.connection, self.currentUserID)
        
        if self.ui.widgetsLayout.count() == 1:
            self.ui.widgetsLayout.itemAt(0).widget().deleteLater()
        self.ui.widgetsLayout.insertWidget(0, widget)
        return
