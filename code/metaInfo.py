# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: metaInfo.py
    :time: 2017/03/13
"""

### 程序根目录 ###
PROGRAMROOTPATH = "/home/dpedw/edwBasicTool/bigdog"
### job日志路径 ###
LOGDIRPATH = PROGRAMROOTPATH + "/log"
taskSubject = 'bigdog task is errors'
## 邮件 相关 ##
class mailVar:
    mailHost = None
    mailUser = None
    mailUserHead = None
    mailUserPassWord = None
    mailPort = None
    taskSubject = None
def setmailHost(mailHost):
    mailVar.mailHost = mailHost
def setmailUser(mailUser):
    mailVar.mailUser = mailUser
def setmailUserHead(mailUserHead):
    mailVar.mailUserHead = mailUserHead
def setmailUserPassWord(mailUserPassWord):
    mailVar.mailUserPassWord = mailUserPassWord
def setmailPort(mailPort):
    mailVar.mailPort = mailPort
def settaskSubject(taskSubject):
    mailVar.taskSubject = taskSubject

def getmailHost():
    return mailVar.mailHost
def getmailUser():
    return mailVar.mailUser
def getmailUserHead():
    return mailVar.mailUserHead
def getmailUserPassWord():
    return mailVar.mailUserPassWord
def getmailPort():
    return mailVar.mailPort
def gettaskSubject():
    return mailVar.taskSubject


### 变动变量 ###
class globalVar:
    vDate = None
    vGroupId = None
    vSnapshot = None
    vLogFilePath = None
    vJobId = None

def setvDate(vDate):
    globalVar.vDate = vDate
def setvGroupId(vGroupId):
    globalVar.vGroupId = vGroupId
def setvSnapshot(vSnapshot):
    globalVar.vSnapshot = vSnapshot
def setvLogFilePath(vLogFilePath):
    globalVar.vLogFilePath = vLogFilePath
def setvJobId(vJobId):
    globalVar.vJobId = vJobId

def getvDate():
    return globalVar.vDate
def getvGroupId():
    return globalVar.vGroupId
def getvSnapshot():
    return globalVar.vSnapshot
def getvLogFilePath():
    return globalVar.vLogFilePath
def getvJobId():
    return globalVar.vJobId
