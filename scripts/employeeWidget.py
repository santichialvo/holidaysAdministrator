# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 19:39:12 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from employeeWidget_ui import Ui_EmployeeWidget
from admDaysDialog_ui import Ui_AdmDaysDialog
from feriadosDialog import feriadosDialog
from restriccionesDialog import restriccionesDialog
from newPeriodDialog import newPeriodDialog
from database_test import getIDCurrentPeriod,searchAllUsersID,searchDaysForUserByID, \
                            searchNameForUserByID,searchforAbsenceOrLicenseByUserID, \
                            searchDaysAcceptedByID,searchDaysByUserID,AddDaysToUser,AddNotification,getUserID,getFeriados

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
    
class employeeWidget(QtWidgets.QWidget):
    def __init__(self,conn,userID):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_EmployeeWidget()
        self.ui.setupUi(self)
        self.connection = conn
        self.currentUserID = userID
        self.daysForEmployee = {}
        self.showEmployeeStatus()
        self.colourRequestedDays()
        self.colourFeriados()
        return
    
    def showEmployeeStatus(self):
        self.ui.employeeStatustableWidget.clearContents()
        self.ui.employeeStatustableWidget.setRowCount(0)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        AllUsersIDs=searchAllUsersID(self.connection)
        Feriados=getFeriados(self.connection,IDCurrentPeriod)
        for UserID in AllUsersIDs:
            Dias=searchDaysForUserByID(self.connection,UserID[0],IDCurrentPeriod)
            Nombre=searchNameForUserByID(self.connection,UserID[0])
            currentRow=self.ui.employeeStatustableWidget.rowCount()
            self.ui.employeeStatustableWidget.setRowCount(currentRow+1)
            it0=QtWidgets.QTableWidgetItem(str(Nombre[0][0] + ' ' + Nombre[0][1]))
            it0.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.employeeStatustableWidget.setItem(currentRow,0,it0)
            DaysTotal=Dias[0][0]
            it1=QtWidgets.QTableWidgetItem(str(DaysTotal))
            it1.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.employeeStatustableWidget.setItem(currentRow,1,it1)
            Absences=searchforAbsenceOrLicenseByUserID(self.connection,UserID[0],IDCurrentPeriod,True)
            DaysAbsences=self.calculateDays(Absences,Feriados)
            it2=QtWidgets.QTableWidgetItem(str(DaysAbsences))
            it2.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.employeeStatustableWidget.setItem(currentRow,2,it2)
            Licenses=searchforAbsenceOrLicenseByUserID(self.connection,UserID[0],IDCurrentPeriod,False)
            DaysLicenses=self.calculateDays(Licenses,Feriados)
            it3=QtWidgets.QTableWidgetItem(str(DaysLicenses))
            it3.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.employeeStatustableWidget.setItem(currentRow,3,it3)
            RestOfDays=DaysTotal-DaysAbsences-DaysLicenses
            it4=QtWidgets.QTableWidgetItem(str(RestOfDays))
            it4.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.employeeStatustableWidget.setItem(currentRow,4,it4)
            color = QtCore.Qt.green if RestOfDays==0 else QtCore.Qt.yellow if RestOfDays>0 else QtCore.Qt.red
            it0.setBackground(color)
        return
    
    def colourFeriados(self):
        format_feriados = QtGui.QTextCharFormat()
        format_feriados.setBackground(QtCore.Qt.blue)
        IDCurrentPeriod = getIDCurrentPeriod(self.connection)
        Feriados = getFeriados(self.connection,IDCurrentPeriod)
        for iFeriados in Feriados:
            self.ui.employeecalendarWidget.setDateTextFormat(iFeriados[0],format_feriados)
        return
    
    def colourRequestedDays(self):
        format_reqday_one = QtGui.QTextCharFormat()
        format_reqday_one.setBackground(QtCore.Qt.yellow)
        format_reqday_two = QtGui.QTextCharFormat()
        format_reqday_two.setBackground(QtCore.Qt.green)
        AllUsersIDs=searchAllUsersID(self.connection)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        daysEmployeeDict = []               #Lista que me indica todos los dias que fueron pedidos
        self.daysForEmployee.clear()        #Diccionario con key=dia_mediodia y value una lista con los id de los empleados
        for idemployee in AllUsersIDs:
            Days = searchDaysAcceptedByID(idemployee[0],self.connection,IDCurrentPeriod)
            for iday in Days:
                if iday[1]!=None:
                    currDay=iday[0]
                    maxDay=iday[1]
                    while currDay<=maxDay:
                        day = QtCore.QDate(currDay.year,currDay.month,currDay.day)
                        color = format_reqday_one if day not in daysEmployeeDict else format_reqday_two
                        self.ui.employeecalendarWidget.setDateTextFormat(day,color)
                        daysEmployeeDict.append(day)
                        key = day.toString()+'_'+str(iday[2]) if iday[2]!=None else day.toString()
                        if key in self.daysForEmployee:
                            self.daysForEmployee[key].append(idemployee[0])
                        else:
                            self.daysForEmployee[key]=[idemployee[0]]
                        currDay += datetime.timedelta(1)
                else:
                    day = QtCore.QDate(iday[0].year,iday[0].month,iday[0].day)
                    color = format_reqday_one if day not in daysEmployeeDict else format_reqday_two
                    self.ui.employeecalendarWidget.setDateTextFormat(day,color)
                    daysEmployeeDict.append(day)
                    key = day.toString()+'_'+str(iday[2]) if iday[2]!=None else day.toString()
                    if key in self.daysForEmployee:
                        self.daysForEmployee[key].append(idemployee[0])
                    else:
                        self.daysForEmployee[key]=[idemployee[0]]
                    
    
    def checkFeriado(self,currDay,Feriados):
        for iFeriado in Feriados:
            if iFeriado[0]==currDay:
                return True
        return False
    
    def calculateDays(self,TupleDays,Feriados):
        Cantidad=0
        for iTuple in TupleDays:
            if iTuple[1] is not None:
                currDay=iTuple[0]
                maxDay=iTuple[1]
                while currDay<=maxDay:
                    if self.checkFeriado(currDay,Feriados):
                        currDay += datetime.timedelta(1)
                        continue
                    if currDay.weekday() not in (5,6):
                        Cantidad+= 1
                    currDay += datetime.timedelta(1)
            else:
                if iTuple[0].weekday() not in (5,6):
                    if self.checkFeriado(iTuple[0],Feriados):
                        continue
                    if iTuple[2]==0:
                        Cantidad+=1
                    else:
                        Cantidad+=0.5
        return Cantidad
    
    def showDaysByEmployee(self,QDate):
        Cadena = ''
        key=QDate.toString()
        key0=QDate.toString()+'_0'
        key1=QDate.toString()+'_1'
        key2=QDate.toString()+'_2'
        if key in self.daysForEmployee:
            for iid in self.daysForEmployee[key]:
                Name = searchNameForUserByID(self.connection,iid)
                Cadena+=(Name[0][0]+' '+Name[0][1]+', ')
            Cadena+='Dia completo \n'
        if key0 in self.daysForEmployee:
            for iid in self.daysForEmployee[key0]:
                Name = searchNameForUserByID(self.connection,iid)
                Cadena+=(Name[0][0]+' '+Name[0][1]+', ')
            Cadena+='Dia completo \n'
        if key1 in self.daysForEmployee:
            for iid in self.daysForEmployee[key1]:
                Name = searchNameForUserByID(self.connection,iid)
                Cadena+=(Name[0][0]+' '+Name[0][1]+', ')
            Cadena+='Medio Día (mañana) \n'
        if key2 in self.daysForEmployee:
            for iid in self.daysForEmployee[key2]:
                Name = searchNameForUserByID(self.connection,iid)
                Cadena+=(Name[0][0]+' '+Name[0][1]+', ')
            Cadena+='Medio Día (tarde) \n'
        if Cadena=='':
            Cadena+='No hay licencias ni ausencias este día'
        
        QtWidgets.QMessageBox.information(self,'Información',Cadena)
        return
    
    def giveDays(self):
        senderButton = self.sender().objectName()
        dialog = QtWidgets.QDialog()
        dialog.setFixedSize(362,280)
        admDialog=Ui_AdmDaysDialog()
        admDialog.setupUi(dialog)
        AllUsersIDs=searchAllUsersID(self.connection)
        
        for UserID in AllUsersIDs:
            Nombre=searchNameForUserByID(self.connection,UserID[0])
            admDialog.employee_comboBox.addItem(Nombre[0][0]+' '+Nombre[0][1])
        
        result=dialog.exec_()
        
        if result:
            dias = admDialog.days_doubleSpinBox.value()
            if (dias % .5!=0):
                QtWidgets.QMessageBox.critical(self,'Error','El número ingresado no es válido')
                return
            
            empleado = admDialog.employee_comboBox.currentText()
            txt = 'agregar ' if senderButton=='giveDays_pushButton' else 'descontar '
            Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea '+str(txt)+str(dias)+' días al empleado '+str(empleado)+'?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if Rta==QtWidgets.QMessageBox.Yes:
                empleado = empleado.split(' ')
                ID_Usuario = getUserID(self.connection,empleado[0],empleado[1])
                IDCurrentPeriod=getIDCurrentPeriod(self.connection)
                DiasOriginal = searchDaysByUserID(self.connection,ID_Usuario,IDCurrentPeriod)
                DiasTotal = DiasOriginal+dias if senderButton=='giveDays_pushButton' else DiasOriginal-dias
                ID_Usuario = getUserID(self.connection,empleado[0],empleado[1])
                Result = AddDaysToUser(self.connection,DiasTotal,ID_Usuario,IDCurrentPeriod)
                if Result==0:
                    QtWidgets.QMessageBox.information(self,'Exito','Operación realizada')
#                    IDCurrentPeriod=getIDCurrentPeriod(self.connection)
                    Razon = str(admDialog.razon_plainTextEdit.toPlainText()) if admDialog.razon_plainTextEdit.toPlainText()!='' else '-'
                    AltaBaja = 1 if senderButton=='giveDays_pushButton' else 0
                    IDUsuario = getUserID(self.connection,empleado[0],empleado[1])
                    AddNotification(self.connection,Razon,str(dias),AltaBaja,IDUsuario,IDCurrentPeriod,self.currentUserID)
                    self.showEmployeeStatus()
                else:
                    QtWidgets.QMessageBox.critical(self,'Error '+str(Result),'No se pudo realizar la operación solicitada')
        return
    
    def resetCalendar(self):
        format_normal = QtGui.QTextCharFormat()
        format_normal.setBackground(QtCore.Qt.white)
        AllUsersIDs=searchAllUsersID(self.connection)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
        # reseteo dias de empleados
        for idemployee in AllUsersIDs:
            Days = searchDaysAcceptedByID(idemployee[0],self.connection,IDCurrentPeriod)
            for iday in Days:
                if iday[1]!=None:
                    currDay=iday[0]
                    maxDay=iday[1]
                    while currDay<=maxDay:
                        day = QtCore.QDate(currDay.year,currDay.month,currDay.day)
                        self.ui.employeecalendarWidget.setDateTextFormat(day,format_normal)
                        currDay += datetime.timedelta(1)
                else:
                    day = QtCore.QDate(iday[0].year,iday[0].month,iday[0].day)
                    self.ui.employeecalendarWidget.setDateTextFormat(day,format_normal)
        # reseteo feriados
        Feriados = getFeriados(self.connection,IDCurrentPeriod)
        for iFeriados in Feriados:
            self.ui.employeecalendarWidget.setDateTextFormat(iFeriados[0],format_normal)
        return
        
    def adminFeriados(self):
        fd = feriadosDialog(self.connection,self.currentUserID,self)
        fd.exec_()
        return
        
    
    def adminRestricciones(self):
        rw = restriccionesDialog(self.connection,self.currentUserID)
        rw.exec_()
        return
    
    def newPeriod(self):
        np = newPeriodDialog(self.connection,self.currentUserID,self)
        np.exec_()
        return