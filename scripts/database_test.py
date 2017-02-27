#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

#from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2

def searchForUsers(user,password,conn):
    cur = conn.cursor()
    command = """SELECT ID from Usuario where Login like '%s' and Password like '%s'"""%(user,password)
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

def doRequestByID(ID_Usuario,conn,FechaD,FechaH=None,Razon=None,MedioDia=None):
    cur = conn.cursor()
    FechaD_S = "'%s/%s/%s'"%(FechaD.day(),FechaD.month(),FechaD.year())
    FechaH_S = 'NULL' if FechaH is None else "'%s/%s/%s'"%(FechaH.day(),FechaH.month(),FechaH.year())
    Razon_S = 'NULL' if Razon is None else Razon
    MedioDia_S = 'NULL' if MedioDia is None else MedioDia
    command = """INSERT into Solicitud values(default,%s,null,%s,%s,'%s','P',%s)"""%(ID_Usuario,FechaD_S,FechaH_S,Razon_S,MedioDia_S)
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
    command = """SELECT ID,Fecha_Desde,Fecha_Hasta,MedioDia,Estado from Solicitud where ID_Usuario_S=%s order by ID"""%ID_Usuario
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
