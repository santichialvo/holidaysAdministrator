#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

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

def searchDaysAcceptedByID(ID_Usuario,conn,ID_Periodo):
    cur = conn.cursor()
    command = """SELECT Fecha_desde,Fecha_hasta,MedioDia from Solicitud where ID_Usuario_S=%s and Estado='A' and ID_Periodo=%s"""%(ID_Usuario,ID_Periodo)
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

def searchRequestsByUserID(ID_Usuario,ID_Periodo,conn,cancel):
    cur = conn.cursor()
    if not cancel:
        command = """SELECT ID,Fecha_Desde,Fecha_Hasta,MedioDia,Tipo,Estado from Solicitud where ID_Usuario_S=%s and ID_Periodo=%s order by ID"""%(ID_Usuario,ID_Periodo)
    else:
        command = """SELECT ID,Fecha_Desde,Fecha_Hasta,MedioDia,Tipo,Estado from Solicitud where ID_Usuario_S=%s and ID_Periodo=%s and (Estado='A' or Estado='P') order by ID"""%(ID_Usuario,ID_Periodo)
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

def searchAllRequests(conn,ID_Periodo):
    cur = conn.cursor()
    command = """SELECT * from Solicitud where ID_Periodo=%s order by ID"""%(ID_Periodo)
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

def addPeriod(conn,Anio):
    cur = conn.cursor()
    command = """INSERT into Periodo values(default,%s,false);"""%(Anio)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def getIDCurrentPeriod(conn):
    cur = conn.cursor()
    command = """SELECT ID from Periodo where Activo=true"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0][0]

def getAnioPeriod(conn,ID):
    cur = conn.cursor()
    command = """SELECT Anio from Periodo where ID=%s"""%(ID)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0][0]

def getAllPeriods(conn):
    cur = conn.cursor()
    command = """SELECT ID from Periodo"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def getIDPeriodByYear(conn,Year):
    cur = conn.cursor()
    command = """SELECT ID from Periodo where Anio=%s"""%(Year)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0][0]

def activate_deactivatePeriod(conn,Anio,activate):
    activateStr='true' if activate else 'false'
    cur = conn.cursor()
    command = """UPDATE Periodo set Activo=%s where Anio=%s"""%(activateStr,Anio)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

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

def searchDaysForUserByID(conn,ID_Usuario,ID_Periodo):
    cur = conn.cursor()
    command = """SELECT Dias from DiasPeriodo where ID_Usuario=%s and ID_Periodo=%s"""%(ID_Usuario,ID_Periodo)
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

def searchDaysByUserID(conn,ID_Usuario,ID_Periodo):
    cur = conn.cursor()
    command = """SELECT Dias from DiasPeriodo where ID_Usuario=%s and ID_Periodo=%s"""%(ID_Usuario,ID_Periodo)
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

def AddDaysToUser(conn,Dias,ID_Usuario,ID_Periodo):
    cur = conn.cursor()
    command = """UPDATE DiasPeriodo set Dias=%s where ID_Usuario=%s and ID_Periodo=%s"""%(Dias,ID_Usuario,ID_Periodo)
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

def addFeriados(conn,ID_Periodo,Fecha,Razon):
    cur = conn.cursor()
    Fecha_S = "'%s/%s/%s'"%(Fecha.day(),Fecha.month(),Fecha.year())
    command = """INSERT into Feriados values(default,%s,'%s',%s)"""%(Fecha_S,Razon,ID_Periodo)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode) #23505 si esta repetido
    conn.commit()
    cur.close()
    return 0

def deleteFeriados(conn,ID_Periodo,Fecha):
    cur = conn.cursor()
    Fecha_S = "'%s/%s/%s'"%(Fecha.day(),Fecha.month(),Fecha.year())
    command = """DELETE from Feriados where ID_Periodo=%s and Fecha=%s"""%(ID_Periodo,Fecha_S)
    try:
        cur.execute(command)
        rows = cur.rowcount
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return rows


def getRestricciones(conn):
    cur = conn.cursor()
    command = """SELECT Usuarios from RestriccionesUsuarios"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def getRestriccionesFromUser(conn,IDUser):
    cur = conn.cursor()
    command = """SELECT Usuarios FROM RestriccionesUsuarios WHERE %s = ANY (Usuarios)"""%(IDUser)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def getRequestByIDs(conn,ID_Req):
    cur = conn.cursor()
    command = """SELECT * from Solicitud where ID=%s"""%(ID_Req)
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0]

def addRestriccionesUsuarios(conn,ResList):
    cur = conn.cursor()
    command = """INSERT into RestriccionesUsuarios values(default,'%s')"""%(ResList)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def deleteRestriccionesUsuarios(conn,ResList):
    cur = conn.cursor()
    command = """DELETE from RestriccionesUsuarios where Usuarios = '%s'"""%(ResList)
    try:
        cur.execute(command)
        rows = cur.rowcount
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return rows

def getPeriodos(conn):
    cur = conn.cursor()
    command = """SELECT Anio FROM Periodo order by ID"""
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows

def getIDPeriodo(conn,year):
    cur = conn.cursor()
    command = """SELECT ID FROM Periodo where Anio=%s"""%year
    cur.execute(command)
    rows = cur.fetchall()
    cur.close()
    return rows[0]

def deletePeriodByYear(conn,year):
    cur = conn.cursor()
    ID=getIDPeriodo(conn,year)
    Commands = []
    Commands.append("""DELETE from Feriados where ID_Periodo=%s"""%ID)
    Commands.append("""DELETE from Notificaciones where ID_Periodo=%s"""%ID)
    Commands.append("""DELETE from Solicitud where ID_Periodo=%s"""%ID)
    Commands.append("""DELETE from DiasPeriodo where ID_Periodo=%s"""%ID)
    Commands.append("""DELETE from Periodo where ID=%s"""%ID)
    for iComm in Commands:
        try:
            cur.execute(iComm)
            rows = cur.rowcount
        except psycopg2.Error as e:
            conn.rollback()
            return int(e.pgcode)
    conn.commit()
    cur.close()
    return rows

def addDaysOnPeriod(conn,ID_Usuario,ID_Periodo):
    cur = conn.cursor()
    command = """INSERT into DiasPeriodo values(default,%s,%s,default)"""%(ID_Usuario,ID_Periodo)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def deleteEmployee(conn,ID):
    cur = conn.cursor()
    Commands = []
    Commands.append("""DELETE from Notificaciones where ID_Usuario=%s"""%ID)
    Commands.append("""DELETE from Solicitud where ID_Usuario_S=%s"""%ID)
    Commands.append("""DELETE from DiasPeriodo where ID_Usuario=%s"""%ID)
    Commands.append("""DELETE from Rol where ID_Usuario=%s"""%ID)
    Commands.append("""DELETE from Usuario where ID=%s"""%ID)
    for iComm in Commands:
        try:
            cur.execute(iComm)
            rows = cur.rowcount
        except psycopg2.Error as e:
            conn.rollback()
            return int(e.pgcode)
    conn.commit()
    cur.close()
    return rows

def addEmployee(conn,nombre,apellido,usuario,password,email):
    cur = conn.cursor()
    command = """INSERT into Usuario values(default,'%s','%s','%s','%s','%s')"""%(usuario,password,nombre,apellido,email)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def createRol(conn,ID,rol):
    cur = conn.cursor()
    cur = conn.cursor()
    Commands = []
    Commands.append("""INSERT into Rol values(default,%s,0)"""%(ID))
    if (rol=='Administrador'):
        Commands.append("""INSERT into Rol values(default,%s,1)"""%(ID))
    for iComm in Commands:
        try:
            cur.execute(iComm)
        except psycopg2.Error as e:
            conn.rollback()
            return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0

def setDaysForNewUser(conn,ID_Usuario,ID_Periodo):
    cur = conn.cursor()
    command = """INSERT into DiasPeriodo values(default,%s,%s,default)"""%(ID_Usuario,ID_Periodo)
    try:
        cur.execute(command)
    except psycopg2.Error as e:
        conn.rollback()
        return int(e.pgcode)
    conn.commit()
    cur.close()
    return 0