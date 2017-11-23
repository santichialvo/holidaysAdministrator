# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:34:36 2017

@author: Santiago
"""
import subprocess

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
