# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: baseMysql.py
    :time: 2017/03/13
"""
import traceback, pymysql

def getConnet(userName, passWord, dbName, port, host):
    try:
        db = pymysql.connect(host=host, port=int(port), user=userName, passwd=passWord, db=dbName)
        return db
    except:
        errors = traceback.format_exc()
        print('baseMysql[getConnet]---> is errors')
        print(errors)
        return "-99999"

def select(userName, passWord, dbName, port, host, sql):
    try:
        #print(sql)
        db = getConnet(userName, passWord, dbName, port, host)
        cur = db.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        db.close()
        return result
    except:
        errors = traceback.format_exc()
        print('baseMysql[select]---> is errors')
        print(errors)
        return "-99999"

def insertDeteleUpdate(userName, passWord, dbName, port, host, sql):
    try:
        #print(sql)
        db = getConnet(userName, passWord, dbName, port, host)
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
        return "0"
    except:
        errors = traceback.format_exc()
        print('baseMysql[select]---> is errors')
        print(errors)
        return "-99999"

def createDrop(userName, passWord, dbName, port, host, sql):
    try:
        db = getConnet(userName, passWord, dbName, port, host)
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.close()
        db.close()
        return "0"
    except:
        errors = traceback.format_exc()
        print('baseMysql[createDrop]---> is errors')
        print(errors)
        return "-99999"
