# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:34:36 2017

@author: Santiago
"""
import subprocess
import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
import datetime

GREEN   = QtCore.Qt.GlobalColor(14)
YELLOW  = QtCore.Qt.GlobalColor(18)
RED     = QtCore.Qt.GlobalColor(13)


def my_assert(obj,cond,errorMsj):
    if not cond:
        QtWidgets.QMessageBox.critical(obj,'Error',errorMsj).exec_()
        sys.exit(1)

# dada una MAC, encontrar su IP en la LAN
def findIPfromMAC(MAC):
    command = 'arp -a | findstr "%s"'%MAC 
    
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    IPstr = str(proc.stdout.read())

    if IPstr!=' ':
        fpos = IPstr.find('192.168')
        IP = ''
        for i in range(fpos,len(IPstr)):
            if (IPstr[i]==' '):
                break
            IP+=IPstr[i]
    return IP

# chequea si es feriado ese dia
def checkFeriado(currDay,Feriados):
        for iFeriado in Feriados:
            if iFeriado[0]==currDay:
                return True
        return False

# calcula la cantidad de días sin feriados entre fechas
def calculateDays(TupleDays,Feriados):
    Cantidad=0
    for iTuple in TupleDays:
        if iTuple[1] is not None:
            currDay=iTuple[0]
            maxDay=iTuple[1]
            while currDay<=maxDay:
                if checkFeriado(currDay,Feriados):
                    currDay += datetime.timedelta(1)
                    continue
#                if currDay.weekday() not in (5,6):
                Cantidad+= 1
                currDay += datetime.timedelta(1)
        else:
#            if iTuple[0].weekday() not in (5,6):
            if checkFeriado(iTuple[0],Feriados):
                continue
            if iTuple[2]==0:
                Cantidad+=1
            else:
                Cantidad+=0.5
    return Cantidad

def getMessagesFont():
    font = QtGui.QFont()
    font.setFamily("Ubuntu")
    font.setPointSize(8)
    return font

def showMessage(content, message_type = 3, buttons = QtWidgets.QMessageBox.Ok):
    # 1 Information, 2 Warning, 3 Critical, 4 Question
    font = getMessagesFont()
    mtitle = 'Información' if message_type==1 else 'Cuidado' if message_type==2 else 'Error' if message_type==3 else 'Pregunta'
    w = QtWidgets.QMessageBox(message_type,mtitle,content,buttons)
    w.setFont(font)
    w.setWindowIcon(QtGui.QIcon(os.path.join(os.environ["HM_INST_DIR"],'images','fromHelyx','mainicon.png')))
    QtWidgets.QApplication.processEvents()
    reply = w.exec_()
    return reply