#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 22:09:21 2017

@author: etekken
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from newPeriodDialog_ui import Ui_NewPeriodDialog
from database_test import getPeriodos,deletePeriodByYear,getIDCurrentPeriod, \
                          getAnioPeriod,activate_deactivatePeriod,addPeriod, \
                          searchAllUsersID,addDaysOnPeriod,getIDPeriodByYear
from utils import my_assert, showMessage
import os

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


class DateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DateDialog, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        
        # comboBox with years
        QtWidgets.QDialog.setWindowTitle(self, 'Nuevo período')
        icon = QtGui.QIcon()
        filename = os.path.join(os.path.join(os.environ["HM_INST_DIR"], 'images', 'fromHelyx', 'mainicon.png'))
        icon.addPixmap(QtGui.QPixmap(filename), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QtWidgets.QDialog.setWindowIcon(self, icon)

        self.yearsComboBox = QtWidgets.QComboBox(self)
        self.yearsComboBox.addItems(['2020', '2021', '2022', '2023', '2024', '2025'])
        layout.addWidget(self.yearsComboBox)

        self.dateEdit = QtWidgets.QDateEdit()
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        layout.addWidget(self.dateEdit)

        # OK and Cancel buttons
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # get current date and time from the dialog
    def periodYear(self):
        return self.yearsComboBox.currentText()

    def getEndDate(self):
        return self.dateEdit.date()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getDateTime(parent=None):
        dialog = DateDialog(parent)
        result = dialog.exec_()
        year = dialog.periodYear()
        end_date = dialog.getEndDate()
        return year, end_date, result == QtWidgets.QDialog.Accepted


class newPeriodDialog(QtWidgets.QDialog):
    def __init__(self, conn, userID, parent):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_NewPeriodDialog()
        self.ui.setupUi(self)
        self.setFixedSize(340, 180)
        self.connection = conn
        self.currentUserID = userID
        self.parent = parent
        self.showPeriods()
        return
    
    def showPeriods(self):
        Periodos = getPeriodos(self.connection)
        self.ui.period_listWidget.clear()
        self.ui.endDateListWidget.clear()
        for iPeriodos in Periodos:
            self.ui.period_listWidget.addItem(str(iPeriodos[0]))
            self.ui.endDateListWidget.addItem(str(iPeriodos[1]))
        self.setActive()
        return
    
    def setActive(self, oldYear=None):
        currentPeriod = getIDCurrentPeriod(self.connection)
        Anio = getAnioPeriod(self.connection, currentPeriod)
        item = self.ui.period_listWidget.findItems(str(Anio), QtCore.Qt.MatchExactly)
        my_assert(self, len(item) == 1, 'El periodo actual sólo puede ser uno. Contacte al administrador.')
        item[0].setFlags(item[0].flags() ^ QtCore.Qt.ItemIsEnabled)
        item_index = self.ui.period_listWidget.row(item[0])
        item_date = self.ui.endDateListWidget.item(item_index)
        item_date.setFlags(item_date.flags() ^ QtCore.Qt.ItemIsEnabled)
        if oldYear:
            item = self.ui.period_listWidget.findItems(str(oldYear), QtCore.Qt.MatchExactly)
            my_assert(self, len(item) == 1, 'El periodo a desactivar sólo puede ser uno. Contacte al administrador.')
            item[0].setFlags(QtCore.Qt.ItemIsEnabled)
            item_index = self.ui.period_listWidget.row(item[0])
            item_date = self.ui.endDateListWidget.item(item_index)
            item_date.setFlags(QtCore.Qt.ItemIsEnabled)
        return
    
    def deletePeriod(self):
        Item = self.ui.period_listWidget.currentItem()
        if not Item:
            showMessage('Debe seleccionar un periodo')
            return
        ItemText = Item.text()
        currentPeriod = getIDCurrentPeriod(self.connection)
        Anio = getAnioPeriod(self.connection, currentPeriod)
        if ItemText == str(Anio):
            showMessage('El periodo a eliminar no puede ser el actual')
            return
        msg = '¿Desea eliminar el periodo '+str(ItemText)+'? Considere que todas las solicitudes y notificaciones serán también eliminadas'
        Rta = showMessage(msg, 4, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if Rta == QtWidgets.QMessageBox.Yes:
            currentPeriod = getIDCurrentPeriod(self.connection)
            Anio = getAnioPeriod(self.connection, currentPeriod)
            if Anio == ItemText:
                showMessage('No puede eliminar el periodo actual')
                return
            rows=deletePeriodByYear(self.connection, ItemText)
            if rows == 1:
                QtWidgets.QMessageBox.information(self, 'Exito', 'Operación realizada')
                self.showPeriods()
            else:
                showMessage('El periodo no pudo ser eliminado')
        return

    def addPeriod(self):
        year, end_date, ok = DateDialog.getDateTime()
        if ok:
            msg = '¿Desea crear el periodo '+str(year)+'?'
            Rta = showMessage(msg, 4, QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            if Rta == QtWidgets.QMessageBox.Yes:
                Res = addPeriod(self.connection, year, end_date)
                if Res == 0:
                    # para cada usuario, insertar sus dias para el respectivo periodo
                    IDs = searchAllUsersID(self.connection)
                    IDPeriod = getIDPeriodByYear(self.connection, year)
                    for ID in IDs:
                        Res = addDaysOnPeriod(self.connection, ID[0], IDPeriod)
                        if Res != 0:
                            showMessage('Error insertando los días del periódo. Contacte con el administrador inmediatamente.')
                            return
                    QtWidgets.QMessageBox.information(self, 'Exito', 'Operación realizada')
                    self.showPeriods()
                elif Res == 23505:
                    showMessage('El periodo ya existe')
                else:
                    showMessage('El periodo no pudo ser creado')
        return
    
    def selectPeriod(self, item):
        newAnio = str(item.text())
        msg = '¿Desea utilizar el periodo '+newAnio+' como activo?'
        Rta = showMessage(msg, 4, QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if Rta == QtWidgets.QMessageBox.Yes:
            currentPeriod = getIDCurrentPeriod(self.connection)
            # reseteo calendario antes de que se cambie el periodo activo
            self.parent.resetCalendar()
            Anio = getAnioPeriod(self.connection, currentPeriod)
            Ret = activate_deactivatePeriod(self.connection, Anio, False)
            if Ret != 0:
                showMessage('La operación no pudo realizarse')
                return
            Ret = activate_deactivatePeriod(self.connection, newAnio, True)
            if Ret != 0:
                showMessage('La operación no pudo realizarse')
                return
            # cambio de periodo activo (en la ventana)
            self.setActive(Anio)
            # vuelvo a cargar las nuevas variables
            self.parent.showEmployeeStatus()
            self.parent.colourRequestedDays()
            self.parent.colourFeriados()
            QtWidgets.QMessageBox.information(self, 'Exito', 'Operación realizada')
        return
