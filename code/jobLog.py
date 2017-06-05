# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import dbConfig, dbConnet, metaInfo, baseModel
import traceback

def deleteJobLog(jobId, executeStep):
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['DELETELOG'].format(metaInfo.getvSnapshot(), metaInfo.getvGroupId(), jobId, metaInfo.getvDate(), executeStep)
        result = dbConnet.insertDeteleUpdate(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        if result == "0":
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        print('jobLog[deleteJobLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def insertJobLog(jobId, executeStep, crontabTime, logPath):
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['INSERTLOG'].format(metaInfo.getvGroupId(), jobId, metaInfo.getvDate(), metaInfo.getvSnapshot(), crontabTime, executeStep, logPath)
        #print(sqlName)
        result = dbConnet.insertDeteleUpdate(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        if result == "0":
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        print('jobLog[insertJobLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def updateJobLog(jobId, executeStep, vStatus, vErrorCode):
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['UPDATELOG'].format(vStatus, vErrorCode, metaInfo.getvSnapshot(), metaInfo.getvGroupId(), jobId, metaInfo.getvDate(), executeStep)
        #print(sqlName)
        result = dbConnet.insertDeteleUpdate(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        if result == "0":
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        #print('jobLog[updateJobLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def deleteGroupLog():
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['DELETEGROUPLOG'].format(metaInfo.getvGroupId(), metaInfo.getvDate(), metaInfo.getvSnapshot())
        result = dbConnet.insertDeteleUpdate(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        if result == "0":
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        print('jobLog[deleteGroupLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def insertGroupLog():
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['INSERTGROUPLOG'].format(metaInfo.getvGroupId(), metaInfo.getvDate(), metaInfo.getvSnapshot())
        result = dbConnet.insertDeteleUpdate(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        if result == "0":
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        print('jobLog[insertGroupLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def updateGroupLog(vStatus, confPv, relaPv, succPv, errPv):
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['UPDATEGROUPLOG'].format(vStatus, metaInfo.getvGroupId(), metaInfo.getvDate(), metaInfo.getvSnapshot(), confPv, relaPv, succPv, errPv)
        #print(sqlName)
        result = dbConnet.insertDeteleUpdate(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        if result == "0":
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        print('jobLog[updateGroupLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def getGroupRunInfo():
    try:
        dbUserName, dbUserPassWord, dbName, dbPort, dbHost = dbConfig.DBINFO[0:]
        dbType = 'mysql'
        sqlName = dbConfig.LOGSQLDICT['groupRunInfo'].format(metaInfo.getvSnapshot(), metaInfo.getvGroupId(), metaInfo.getvDate())
        result = dbConnet.select(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, sqlName)
        return result[0]
    except:
        errors = traceback.format_exc()
        print('jobLog[updateGroupLog] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

