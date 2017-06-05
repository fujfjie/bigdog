# -*- coding: utf-8 -*-
import time, os, codecs, traceback, datetime
#
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: baseModel.py
    :time: 2017/03/13
"""

'''
desc
    init[0001]:
        输入字符串日期，输出周几
        dateType         str    seconds\hours\days\weeks
param
    init[0001]:
        dateString             str          日期
        dateFormat             str          日期格式
return
    init[0001]:
        result                 datetime     日期
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2017-02-08
'''
def getDatetimeFromString(dateString, dateFormat):
    try:
        return datetime.datetime.strptime(dateString, dateFormat)
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        日期转化成字符串
param
    init[0001]:
        dataTimePara        time        日期
        forMat              str         返回格式
return
    init[0001]:
        日期格式            str   正常
        -99999              str   异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-12
'''
def getTimeFormat(dataTimePara = time.time(), forMat = '%Y%m%d'):
    try:
        return time.strftime(forMat, time.localtime(dataTimePara))
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        写文件函数
param
    init[0001]:
        filePath        str         文件路径
        contents        list|str    内容
         modeFile       str        模式
return
    init[0001]:
        0               正常
        "-99999"        异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-12
'''
def setWriteContentList(filePath, contents, modeFile):
    try:
        wFile = codecs.open(filePath, modeFile, encoding='utf8') ###采用utf8打开文件
        if isinstance(contents, list):
            wFile.writelines(contents) ###写文件内容
        else:
            wFile.write(str(contents)) ###转化成字符串写入
        wFile.close() ###关闭文件
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        初始化：创建目录
param
    init[0001]:
        dirPathName         str         目录绝对路径
return
    init[0001]:
        "0"               正常
        "-99999"        异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-12
'''
def mkdir(dirPathName):
    try:
        os.mkdir(dirPathName)
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        是否存在文件夹，存在不创建，不存在创建
param
    init[0001]:
        dirPathName         str         目录绝对路径
return
    init[0001]:
        0                   str             正常
        "-99999"            str             异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-12
'''
def existeFolder(dirPathName):
    try:
        if os.path.isdir(dirPathName):
            pass
        else:
            mkdir(dirPathName)
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        读取文件大小
param
    init[0001]:
        filePath        str         文件路径
return
    init[0001]:
        文件内容         list        正常
        "-99999"         str        异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-13
'''
def getFileContents(filePath):
    try:
        rFile = codecs.open(filePath, 'r', encoding='utf8') ###采用utf8打开文件
        result = rFile.readlines()
        return result
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        短信告警
param
    init[0001]:
        msgId           str         文件路径
        msgPasswd       str         短信密码
        contents        str         短信内容
return
    init[0001]:
        "0"             str         正常
        "-99999"        str         异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-13
'''
def sendMsgInfo(msgSubject, sendMail, textContent = None, htmlContent = None, attFilePath = None):
    try:
        import baseMail
        result = baseMail.sendMail(msgSubject, sendMail, textContent, htmlContent, attFilePath)
        return result
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        创建文件
param
    init[0001]:
        filePathName    str     文件名称
return
    init[0001]:
        "0"             str         正常
        "-99999"        str         异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-13
'''
def touchFile(filePathName):
    try:
        rFile = codecs.open(filePathName, 'w', encoding='utf8') ###采用utf8打开文件
        rFile.close()
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        文件存在不创建，文件不存在创建
param
    init[0001]:
        filePathName    str     文件名称
return
    init[0001]:
        "0"             str         正常
        "-99999"        str         异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-13
'''
def existeFile(filePathName):
    try:
        if os.path.isfile(filePathName):
            pass
        else:
            touchFile(filePathName)
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        文件存在删除
param
    init[0001]:
        filePathName    str     文件名称
return
    init[0001]:
        "0"             str         正常
        "-99999"        str         异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-20
'''
def rmFile(filePathName):
    try:
        if os.path.isfile(filePathName):
            os.remove(filePathName)
        else:
            print('the file does not exist')
        return "0"
    except:
        errors = traceback.format_exc()
        print(errors)
        return "-99999"
'''
desc
    init[0001]:
        输入一个日期字符串、时间差，输出时间格式字符串
        dateType         str    seconds\hours\days\weeks
param
    init[0001]:
        sourDateString    str     源日期字符串
        sourDateFormat    str     源日期字符串格式
        tarDateFormat     str     输出日期字符串格式
        days              str     时间差
return
    init[0001]:
        "0"             str         正常
        "-99999"        str         异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2016-10-20
'''
def getDateForMat(sourDateString, sourDateFormat, tarDateFormat, dateType, times):
    try:
        sourDate = getDatetimeFromString(sourDateString, sourDateFormat)
        tagDate = eval('sourDate + datetime.timedelta(%s=%d)' % (dateType, times))
        resultTag = datetime.datetime.strftime(tagDate, tarDateFormat)
        return resultTag
    except:
        errors = traceback.format_exc()
        print(errors)
        print('getDateForMat---->execute is errors')
        return "-99999"
'''
desc
    init[0001]:
        对比两个文件是否内容一致
        dateType         str    seconds\hours\days\weeks
param
    init[0001]:
        filePathName           str     文件
        compareFilePathName    str     对比文件
return
    init[0001]:
        "0"             str         正常
        "-99999"        str         异常
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2017-01-10
'''
def getCompareFile(filePathName, compareFilePathName):
    try:
        tmpFileContent = getFileContents(filePathName)
        tmpCompareFileContent = getFileContents(compareFilePathName)
        tmpFileContent.sort()
        tmpCompareFileContent.sort()
        if tmpFileContent == tmpCompareFileContent: ### 两个list相同
            return "0"
        else:
            return "-99999"
    except:
        errors = traceback.format_exc()
        print(errors)
        print('getCompareFile---->execute is errors')
        return "-99999"
'''
desc
    init[0001]:
        输入字符串日期，输出周几
        dateType         str    seconds\hours\days\weeks
param
    init[0001]:
        dateString             str     日期
        dateFormat             str     日期格式
return
    init[0001]:
        result                 str     周几
author
    init[0001]:
        fisher.jie
time
    init[0001]:
        2017-02-08
'''
def getWeekDay(dateString, dateFormat):
    weekDayDict = {
        0: '1',
        1: '2',
        2: '3',
        3: '4',
        4: '5',
        5: '6',
        6: '7',
    }
    tmpDataTime = getDatetimeFromString(dateString, dateFormat)
    return weekDayDict[tmpDataTime.weekday()]


# print(getWeekDay('20170209','%Y%m%d'))
