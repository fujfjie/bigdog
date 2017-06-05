# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import traceback,  baseMysql
def getDb(*keys):
    try:
        dbType, userName, passWord, dbName, port, host, charset = [ i.encode() for i in keys ]
        if dbType == 'mysql':
            return baseMysql.getConnet(userName, passWord, dbName, port, host, charset)
    except:
        errors = traceback.format_exc()
        print('dbConnet[getDb]---> is errors')
        print(errors)
        return "-99999"

def select(*keys):
    try:
        dbType, userName, passWord, dbName, port, host, charset, sql = [ i.encode() for i in keys ]
        if dbType == 'mysql':
            return baseMysql.select(userName, passWord, dbName, port, host, charset, sql)
    except:
        errors = traceback.format_exc()
        print('dbConnet[select]---> is errors')
        print(errors)
        return "-99999"

def insertDeteleUpdate(*keys):
    try:
        dbType, userName, passWord, dbName, port, host, charset, sql = [ i.encode() for i in keys ]
        if dbType == 'mysql':
            return baseMysql.insertDeteleUpdate(userName, passWord, dbName, port, host, charset, sql)
    except:
        errors = traceback.format_exc()
        print('dbConnet[insertDeteleUpdate]---> is errors')
        print(errors)
        return "-99999"

def createDrop(*keys):
    try:
        dbType, userName, passWord, dbName, port, host, charset, sql = [ i.encode() for i in keys ]
        if dbType == 'mysql':
            return baseMysql.createDrop(userName, passWord, dbName, port, host, charset, sql)
    except:
        errors = traceback.format_exc()
        print('dbConnet[insertDeteleUpdate]---> is errors')
        print(errors)
        return "-99999"
