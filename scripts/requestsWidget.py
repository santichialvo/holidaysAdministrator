# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:02:54 2017

@author: Santiago
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from requestsWidget_ui import Ui_RequestsWidget
from database_test import searchNameByRequest,searchAllRequests,updateRequestStatus, \
                          getRestriccionesFromUser,getRequestByIDs,searchforAbsenceOrLicenseByUserID, \
                          getIDCurrentPeriod,searchNameForUserByID

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
    
class requestsWidget(QtWidgets.QWidget):
    def __init__(self,conn,userID):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_RequestsWidget()
        self.ui.setupUi(self)
        self.connection = conn
        self.currentUserID = userID
        self.showRequestsAdm()
        return
    
    def showRequestsAdm(self):
        Requests = searchAllRequests(self.connection)
        self.ui.tableAdmSolicitudes.clearContents()
        self.ui.tableAdmSolicitudes.setRowCount(0)
        for irequest in Requests:
            currentRow=self.ui.tableAdmSolicitudes.rowCount()
            self.ui.tableAdmSolicitudes.setRowCount(currentRow+1)
            it0=QtWidgets.QTableWidgetItem(str(irequest[0]))
            it0.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,0,it0)
            Tuple=searchNameByRequest(irequest[0],False,self.connection)
            it1=QtWidgets.QTableWidgetItem(str(Tuple[0][0]+' '+Tuple[0][1]))
            it1.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,1,it1)
            it2=QtWidgets.QTableWidgetItem(str(irequest[3].day)+'/'+str(irequest[3].month)+'/'+str(irequest[3].year))
            it2.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,2,it2)
            it3=QtWidgets.QTableWidgetItem(str(irequest[4].day)+'/'+str(irequest[4].month)+'/'+str(irequest[4].year) if irequest[4] is not None else '-')
            it3.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,3,it3)
            it4=QtWidgets.QTableWidgetItem(str('Día completo') if irequest[7]==0 else str('Medio día (mañana)') if irequest[7]==1 else str('Medio día (tarde)') if irequest[7]==2 else str('-'))
            it4.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,4,it4)
            it5=QtWidgets.QTableWidgetItem(str('Licencia') if irequest[8]==0 else str('Ausencia'))
            it5.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            color = QtCore.Qt.darkYellow if irequest[8]==0 else QtCore.Qt.darkGreen
            it5.setBackground(color)
            self.ui.tableAdmSolicitudes.setItem(currentRow,5,it5)
            it6=QtWidgets.QTableWidgetItem(str(irequest[5]) if irequest[5]!=None and irequest[5]!='NULL' else str('-'))
            it6.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,6,it6)
            it7=QtWidgets.QTableWidgetItem(str('Pendiente') if irequest[6]=='P' else str('Aprobada') if irequest[6]=='A' else str('Rechazada'))
            it7.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            color = QtCore.Qt.red if irequest[6]=='R' else QtCore.Qt.yellow if irequest[6]=='P' else QtCore.Qt.green
            it7.setBackground(color)
            self.ui.tableAdmSolicitudes.setItem(currentRow,7,it7)
            Tuple=searchNameByRequest(irequest[0],True,self.connection)
            if Tuple:
                it8=QtWidgets.QTableWidgetItem(str(Tuple[0][0]+' '+Tuple[0][1]))
            else:
                it8=QtWidgets.QTableWidgetItem(str('-'))
            it8.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
            self.ui.tableAdmSolicitudes.setItem(currentRow,8,it8)
        return
    
    def verifyRestriccion(self,RequestNumber):
        Request = getRequestByIDs(self.connection,RequestNumber)
        RequestAux = [(Request[3],Request[4],Request[7])]
        UserID = Request[1]
        UserRestricciones = getRestriccionesFromUser(self.connection,UserID)
        IDCurrentPeriod=getIDCurrentPeriod(self.connection)
#        AusenciasUser = searchforAbsenceOrLicenseByUserID(self.connection,UserID,IDCurrentPeriod,True)
#        LicenciasUser = searchforAbsenceOrLicenseByUserID(self.connection,UserID,IDCurrentPeriod,False)
        VecRes = []
        for iUserRestricciones in UserRestricciones:
            iUserRestricciones = iUserRestricciones[0]
            for ijUserRestricciones in iUserRestricciones:
                if ijUserRestricciones==UserID:
                    continue
                AusenciasUserRes = searchforAbsenceOrLicenseByUserID(self.connection,ijUserRestricciones,IDCurrentPeriod,True)
                LicenciasUserRes = searchforAbsenceOrLicenseByUserID(self.connection,ijUserRestricciones,IDCurrentPeriod,False)
                if self.checkCollisionsOnRestricciones(LicenciasUserRes,RequestAux):
                    VecRes.append(iUserRestricciones)
                    break
                if self.checkCollisionsOnRestricciones(AusenciasUserRes,RequestAux):
                    VecRes.append(iUserRestricciones)
                    break
        return VecRes
    
    def auxCheckCollisionOnResitricciones(self,iALUser,iALUserRes):
        # si ambas no tienen fecha_hasta, es por un dia. Hay que chequear que 
        # no sean ambas por la tarde o mañana
        if (iALUser[1]==None and iALUserRes[1]==None):
            if (iALUser[0]==iALUserRes[0]):
                # si coinciden en mañana, tarde o todo el día
                if (iALUser[2]==iALUserRes[2]):
                    return True
        # si solo una no tiene fecha hasta, chequear que esa no este entre 
        # las otras dos, ida y vuelta
        if (iALUser[1]==None and iALUserRes[1]!=None):
            if (iALUserRes[0] <= iALUser[0] <= iALUserRes[1]):
                return True
        if (iALUserRes[1]==None and iALUser[1]!=None):
            if (iALUser[0] <= iALUserRes[0] <= iALUser[1]):
                return True

        # si ambas tienen fecha_hasta, chequear que los intervalos no se superpongan
        if (iALUser[1] != None and iALUserRes[1] != None):
            if ( (iALUser[0] <= iALUserRes[0] <= iALUser[1]) or (iALUser[0] <= iALUserRes[1] <= iALUser[1]) ):
                    return True
        if (iALUserRes[1] != None and iALUser[1] != None):
            if ( (iALUserRes[0] <= iALUser[0] <= iALUserRes[1]) or (iALUserRes[0] <= iALUser[1] <= iALUserRes[1]) ):
                    return True
        
        return False
    
    
    def checkCollisionsOnRestricciones(self,ALUserRes,ALUser):
        for iALUserRes in ALUserRes:
            for iALUser in ALUser:
                 if self.auxCheckCollisionOnResitricciones(iALUser,iALUserRes):
                     return True
        return False
    
    def aprobeRequest(self):
        if self.ui.tableAdmSolicitudes.currentRow()>=0:
            RequestNumber=str(self.ui.tableAdmSolicitudes.item(self.ui.tableAdmSolicitudes.currentRow(),0).text())
            VecRes = self.verifyRestriccion(RequestNumber)
            print VecRes
            if VecRes != []:
                names = ''
                for iVecRes in VecRes:
                    for ijVecRes in iVecRes:
                        User = searchNameForUserByID(self.connection,ijVecRes)
                        names = names + User[0][0] + ' ' + User[0][1] + ', '
                    names = names[:-2] if names != '' else names
                    names = names + ' - '
                names = names[:-3] if names != '' else names
                Rta = QtWidgets.QMessageBox.question(self,'Cuidado','Está por aprobar una solicitud que viola una restricción: %s ¿Desea continuar?'%(names),QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
                if Rta==QtWidgets.QMessageBox.No:
                    QtWidgets.QMessageBox.critical(self,'Cancelar','Aprobación cancelada')
                    return
            Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea aprobar la solicitud %s?'%RequestNumber,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if Rta==QtWidgets.QMessageBox.Yes:
                Return=updateRequestStatus(RequestNumber,False,self.currentUserID,self.connection)
                if Return==0:
                    QtWidgets.QMessageBox.information(self,'Exito','Aprobación confirmada')
                    self.showRequestsAdm()
            else:
                QtWidgets.QMessageBox.critical(self,'Cancelar','Aprobación cancelada')
        else:
            QtWidgets.QMessageBox.critical(self,'Error','Debe seleccionar una solicitud')
        return
    
    def cancelRequest(self):
        if self.ui.tableAdmSolicitudes.currentRow()>=0:
            RequestNumber=str(self.ui.tableAdmSolicitudes.item(self.ui.tableAdmSolicitudes.currentRow(),0).text())
            Rta = QtWidgets.QMessageBox.question(self,'Confirmación','¿Desea cancelar la solicitud %s?'%RequestNumber,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if Rta==QtWidgets.QMessageBox.Yes:
                Return=updateRequestStatus(RequestNumber,True,self.currentUserID,self.connection)
                if Return==0:
                    QtWidgets.QMessageBox.information(self,'Exito','Cancelación confirmada')
                    self.showRequestsAdm()
            else:
                QtWidgets.QMessageBox.critical(self,'Cancelar','Cancelación rechazada')
        else:
            QtWidgets.QMessageBox.critical(self,'Error','Debe seleccionar una solicitud')
        return