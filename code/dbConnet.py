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
        if keys[0] == 'mysql':
            userName, passWord, dbName, port, host = keys[1:]
            return baseMysql.getConnet(userName, passWord, dbName, port, host)
    except:
        errors = traceback.format_exc()
        print('dbConnet[getDb]---> is errors')
        print(errors)
        return "-99999"

def select(*keys):
    try:
        if keys[0] == 'mysql':
            userName, passWord, dbName, port, host, sql = keys[1:]
            return baseMysql.select(userName, passWord, dbName, port, host, sql)
    except:
        errors = traceback.format_exc()
        print('dbConnet[select]---> is errors')
        print(errors)
        return "-99999"

def insertDeteleUpdate(*keys):
    try:
        if keys[0] == 'mysql':
            userName, passWord, dbName, port, host, sql = keys[1:]
            return baseMysql.insertDeteleUpdate(userName, passWord, dbName, port, host, sql)
    except:
        errors = traceback.format_exc()
        print('dbConnet[insertDeteleUpdate]---> is errors')
        print(errors)
        return "-99999"

def createDrop(*keys):
    try:
        if keys[0] == 'mysql':
            userName, passWord, dbName, port, host, sql = keys[1:]
            return baseMysql.createDrop(userName, passWord, dbName, port, host, sql)
    except:
        errors = traceback.format_exc()
        print('dbConnet[insertDeteleUpdate]---> is errors')
        print(errors)
        return "-99999"

