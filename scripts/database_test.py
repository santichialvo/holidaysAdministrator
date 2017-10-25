#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

#from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2

def searchForUsers(user,password,conn):
    cur = conn.cursor()
    command = """SELECT ID_Usuario from Rol r inner join Usuario u on u.ID = r.ID_Usuario where u.Login like '%s' and u.Password like '%s'"""%(user,password)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchUserByID(ID,conn):
    cur = conn.cursor()
    command = """SELECT * from Usuario where ID=%s"""%(ID)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchDaysAcceptedByID(ID_Usuario,conn):
    cur = conn.cursor()
    command = """SELECT Fecha_desde,Fecha_hasta,MedioDia from Solicitud where ID_Usuario_S=%s and Estado='A'"""%ID_Usuario
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def doRequestByID(ID_Usuario,conn,FechaD,Tipo,ID_Periodo,FechaH=None,Razon=None,MedioDia=None):
    cur = conn.cursor()
    FechaD_S = "'%s/%s/%s'"%(FechaD.day(),FechaD.month(),FechaD.year())
    FechaH_S = 'NULL' if FechaH is None else "'%s/%s/%s'"%(FechaH.day(),FechaH.month(),FechaH.year())
    Razon_S = 'NULL' if Razon is None else Razon
    MedioDia_S = 'NULL' if MedioDia is None else MedioDia
    command = """INSERT into Solicitud values(default,%s,null,%s,%s,'%s','P',%s,%s,%s)"""%(ID_Usuario,FechaD_S,FechaH_S,Razon_S,MedioDia_S,Tipo,ID_Periodo)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode) #23505
    conn.commit()
    cur.close()
    return 0

def searchRequestsByUserID(ID_Usuario,conn):
    cur = conn.cursor()
    command = """SELECT ID,Fecha_Desde,Fecha_Hasta,MedioDia,Tipo,Estado from Solicitud where ID_Usuario_S=%s order by ID"""%ID_Usuario
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchRequestByIDs(ID_Req,ID_Usuario,conn):
    cur = conn.cursor()
    command = """SELECT * from Solicitud where ID=%s and ID_Usuario_S=%s"""%(ID_Req,ID_Usuario)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def deleteRequestByID(ID_Req,conn):
    cur = conn.cursor()
    command = """DELETE from Solicitud where ID=%s"""%ID_Req
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def searchAllRequests(conn):
    cur = conn.cursor()
    command = """SELECT * from Solicitud order by ID"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchNameByRequest(ID_Req,Admin,conn):
    Admin_S = 'ID_Usuario_A' if Admin else 'ID_Usuario_S'
    cur = conn.cursor()
    command = """SELECT u.Nombre,u.Apellido from Solicitud s inner join Usuario u on u.ID = s.%s where s.ID = %s"""%(Admin_S,ID_Req)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def getIDCurrentPeriod(conn):
    cur = conn.cursor()
    command = """SELECT ID from Periodo order by ID desc limit 1"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0][0]

def updateRequestStatus(ID_Req,Cancel,ID_Admin,conn):
    cur = conn.cursor()
    Cancel_S = 'R' if Cancel else 'A'
    command = """UPDATE Solicitud set Estado='%s',ID_Usuario_A=%s where ID=%s"""%(Cancel_S,ID_Admin,ID_Req)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def searchAllUsersID(conn):
    cur = conn.cursor()
    command = """SELECT ID from Usuario order by ID"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchDaysForUserByID(conn,ID_Usuario):
    cur = conn.cursor()
    command = """SELECT Dias from Usuario where ID=%s"""%ID_Usuario
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchNameForUserByID(conn,ID_Usuario):
    cur = conn.cursor()
    command = """SELECT Nombre,Apellido from Usuario where ID=%s"""%ID_Usuario
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchforAbsenceOrLicenseByUserID(conn,ID_Usuario,ID_Periodo,Ausencia):
    Tipo = 1 if Ausencia else 0
    cur = conn.cursor()
    command = """SELECT Fecha_Desde,Fecha_Hasta,MedioDia from Solicitud where ID_Usuario_S=%s and ID_Periodo=%s and Tipo=%s and Estado='A'"""%(ID_Usuario,ID_Periodo,Tipo)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchDaysByUserID(conn,Nombre_Usuario,Apellido_Usuario):
    cur = conn.cursor()
    command = """SELECT Dias from Usuario where Nombre like '%s' and Apellido like '%s'"""%(Nombre_Usuario,Apellido_Usuario)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0][0]

def getUserID(conn,Nombre_Usuario,Apellido_Usuario):
    cur = conn.cursor()
    command = """SELECT ID from Usuario where Nombre like '%s' and Apellido like '%s'"""%(Nombre_Usuario,Apellido_Usuario)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0][0]

def AddDaysToUser(conn,Dias,Nombre_Usuario,Apellido_Usuario):
    cur = conn.cursor()
    command = """UPDATE Usuario set Dias=%s where Nombre like '%s' and Apellido like '%s'"""%(Dias,Nombre_Usuario,Apellido_Usuario)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def searchAllNotifications(conn,ID_Periodo):
    cur = conn.cursor()
    command = """SELECT Fecha,Razon,ID_Usuario,Cantidad,AltaBaja,ID_Admin from Notificaciones where ID_Periodo = %s order by ID"""%ID_Periodo
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def searchNotificationsByID(conn,ID_Periodo,ID_Usuario):
    cur = conn.cursor()
    command = """SELECT Fecha,Razon,Cantidad,AltaBaja,ID_Admin from Notificaciones where ID_Periodo = %s and ID_Usuario = %s order by ID"""%(ID_Periodo,ID_Usuario)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def getFeriados(conn,ID_Periodo):
    cur = conn.cursor()
    command = """SELECT Fecha,Motivo from Feriados where ID_Periodo = %s order by Fecha"""%(ID_Periodo)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def AddNotification(conn,Razon,Dias,AltaBaja,ID_Usuario,ID_Periodo,ID_Admin):
    cur = conn.cursor()
    command = """INSERT into Notificaciones values(default,current_timestamp,'%s',%s,%s,%s,%s,%s)"""%(Razon,Dias,AltaBaja,ID_Periodo,ID_Usuario,ID_Admin)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode) #23505
    conn.commit()
    cur.close()
    return 0