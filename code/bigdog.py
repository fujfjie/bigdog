# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import baseModel, metaInfo, dbConfig, dbConnet 
import passwordAes
import traceback
## job 信息 ##
JOBINFODICT = {}
## 依赖关系 ##
STARTJOBRELATIONDICT = {}
## 被依赖关系 ##
JOBRELATIONDICT = {}
## 组信息 ##
GROUPINFO = []
## push mail 信息 ##
PUSHMAIL = []
def getDeleteStartJobRela(vGroupId, vDate, vSnapshot, jobId):
    try:
        global STARTJOBRELATIONDICT, JOBRELATIONDICT
        if jobId in JOBRELATIONDICT.keys():
            for i in JOBRELATIONDICT[jobId]:
                if i not in STARTJOBRELATIONDICT.keys():
                    STARTJOBRELATIONDICT[i] = [jobId]
                else:
                    if jobId not in STARTJOBRELATIONDICT[i]:
                        if STARTJOBRELATIONDICT[i] == []:
                            STARTJOBRELATIONDICT[i].append(jobId)
                        else:
                            STARTJOBRELATIONDICT[i] = [jobId]
                getDeleteStartJobRela(vGroupId, vDate, vSnapshot, i)
    except:
        errors = traceback.format_exc()
        print(errors)
    
def getOraleInfo():
    try: 
        global STARTJOBRELATIONDICT, JOBRELATIONDICT, JOBINFODICT, GROUPINFO, PUSHMAIL
        dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, charset = dbConfig.DBINFO[0:]
        for key, value in dbConfig.SQLDICT.items():
            if key == "JOBINFO":
                sqlName = value.format(metaInfo.getvSnapshot(), metaInfo.getvGroupId(), metaInfo.getvDate())
                #print(sqlName)
                sqlResult = dbConnet.select(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, charset, sqlName)
                for i in sqlResult:
                    jobId, jobName, jobPath, executeTime, executeDay, retryCount, ruleName, mailList, statusId = i
                    if jobId not in JOBINFODICT.keys():
                        JOBINFODICT[jobId] = [jobName, jobPath, executeTime, executeDay, retryCount, ruleName, mailList, statusId]
                    else:
                        print("调度有重复----->" + str(jobId))
            elif key == "STARTJOBRELATION":
                sqlName = value.format(metaInfo.getvGroupId())
                #print(sqlName)
                sqlResult = dbConnet.select(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, charset, sqlName)
                for i in sqlResult:
                    startJobId, jobList = i
                    if startJobId not in STARTJOBRELATIONDICT.keys():
                        STARTJOBRELATIONDICT[startJobId] = []
                        if jobList is not None:
                            for tmpI in jobList.split(','):
                                STARTJOBRELATIONDICT[startJobId].append(int(tmpI))
                    else:
                        print("STARTJOBRELATIONDICT[依赖关系有重复]---->" + str(startJobId))
                #print(STARTJOBRELATIONDICT)
            elif key == 'pushMailInfo':
                sqlName = value
                sqlResult = dbConnet.select(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, charset, sqlName)
                for i in sqlResult:
                    mailHost, mailUser, mailUserHead, mailUserPassword, mailPort, mailSubject = i
                    pc = passwordAes.prpcrypt('f$Jun%big@Dog!fisher.jie') 
                    mailUserPassword = pc.decrypt(mailUserPassword)
                    PUSHMAIL = [mailHost, mailUser, mailUserHead, mailUserPassword, mailPort, mailSubject]#passwordAes.aes_decrypt('f$Jun%big@Dog!fisher.jie',mailUserPassword), mailPort, mailSubject]
            elif key == "JOBRELATION":
                sqlName = value.format(metaInfo.getvGroupId())
                #print(sqlName)
                sqlResult = dbConnet.select(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, charset, sqlName)
                for i in sqlResult:
                    startJobId, jobList = i
                    if startJobId not in JOBRELATIONDICT.keys():
                        JOBRELATIONDICT[startJobId] = []
                        for tmpI in jobList.split(','):
                            JOBRELATIONDICT[startJobId].append(int(tmpI))
                    else:
                        print("JOBRELATION[依赖关系有重复]---->" + str(startJobId))
                #print(JOBRELATIONDICT)
            elif key == "GROUPINFO":
                sqlName = value.format(metaInfo.getvGroupId())
                #print(sqlName)
                sqlResult = dbConnet.select(dbType, dbUserName, dbUserPassWord, dbName, dbPort, dbHost, charset, sqlName)
                for i in sqlResult:
                    groupName, parallelNums, retryCount, mainList = i
                    GROUPINFO = [groupName, parallelNums, retryCount, mainList]
                #print(GROUPINFO)
        if metaInfo.getvJobId() is not None:
            tmpJobId = int(metaInfo.getvJobId())
            for key, value in JOBINFODICT.items():
                JOBINFODICT.pop(key)
                jobName, jobPath, executeTime, executeDay, retryCount, ruleName, mailList, statusId = value
                JOBINFODICT[key] = [jobName, jobPath, executeTime, executeDay, retryCount, ruleName, mailList, 4]
            STARTJOBRELATIONDICT = {}
            STARTJOBRELATIONDICT[tmpJobId] = []
            getDeleteStartJobRela(metaInfo.getvGroupId(), metaInfo.getvDate(), metaInfo.getvSnapshot(), tmpJobId)
        print(STARTJOBRELATIONDICT)
        print(JOBRELATIONDICT)
    except:
        errors = traceback.format_exc()
        print(errors)

def setMkdirDir():
    try:
        ### 创建目录 ###
        baseModel.existeFolder(metaInfo.LOGDIRPATH + '/' + metaInfo.getvDate())
        baseModel.existeFolder(metaInfo.LOGDIRPATH + '/' + metaInfo.getvDate() + '/' + metaInfo.getvGroupId())
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
def initStart():
    try:
        ### 创建目录###
        setMkdirDir()
        ### 获取 基础信息 ###
        getOraleInfo()
    except:
        errors = traceback.format_exc()
        print(errors)
