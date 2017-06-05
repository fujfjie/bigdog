# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import multiprocessing, traceback, time, baseModel, jobLog, bigdog, metaInfo
class Producer(multiprocessing.Process):
    def __init__(self, tmpStartJobRelation, workQueue, vGroupId, vDate, vSnapshot, successQueue, errorQueue, taskStatusDist, producerOver):
        multiprocessing.Process.__init__(self)
        self.jobRelationDict = tmpStartJobRelation
        self.queue = workQueue
        self.vGroupId = vGroupId
        self.vDate = vDate
        self.vSnapshot = vSnapshot
        self.successQueue = successQueue
        self.errorQueue = errorQueue
        self.taskStatusDist = taskStatusDist
        self.producerOver = producerOver
    ### 判断是否满足周 天 ###
    def compareWeek(self, executeDay):
        try:
            weekDay = baseModel.getWeekDay(self.vDate, '%Y%m%d') ### 获取周几 ###
            if weekDay in executeDay.split(','):### 需要执行 ###
                return "0"
            else:### 不需要执行 ###
                return "-1"
        except:
            errors = traceback.format_exc()
            print('Producer[compareWeek] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"
    ### 判断是否满足月 天 ###
    def compareMonth(self, executeDay):
        try:
            if str(int(self.vDate[6:8])) in executeDay.split(','): ### 需要执行 ###
                return "0"
            else:### 不需要执行 ###
                return "-1"
        except:
            errors = traceback.format_exc()
            print('Producer[compareMonth] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"
    ### 判断时间规则是否ok ###
    def compareTimeRule(self, executeDay, ruleName):
        try:
            if ruleName == 'DAY': ### 天执行 ###
                return "0"
            elif ruleName == 'WEEK': ### 周执行 ###
                return Producer.compareWeek(self, executeDay)
            elif ruleName == 'MONTH': ### 月执行 ###
                return Producer.compareMonth(self, executeDay)
            elif ruleName == 'ODDDAY': ### 逢单号执行 ###
                if int(self.vDate[6:8]) % 2 == 1:
                    return "0"
                else:
                    return "-1"
            elif ruleName == 'EVENDAY': ### 逢双号执行 ###
                if int(self.vDate[6:8]) % 2 == 0:
                    return "0"
                else:
                    return "-1"
            elif ruleName == 'LASTDAY': ### 月末最后一天执行###
                if baseModel.getDateForMat(self.vDate, '%Y%m%d', '%d', 'days', 1) == "01":
                    return "0"
                else:
                    return "-1"
            elif ruleName == 'FIRSTDAY': ### 月第一号执行 ###
                if self.vDate[6:8] == "01":
                    return "0"
                else:
                    return "-1"
            elif ruleName == 'WORKDAY': ### 排除周六周日 ###
                if baseModel.getWeekDay(self.vDate, '%Y%m%d') not in('6', '7'):
                    return "0"
                else:
                    return "-1"
        except:
            errors = traceback.format_exc()
            print('Producer[compareTimeRule] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"
    ### 系统时间与配置时间比较 ###
    def compareTimes(self, executeTime, ruleName, executeDay):
        try:
            hour, minute, second = executeTime.split(':')
            realhour, realminute, realsecond = time.strftime('%H:%M:%S', time.localtime()).split(':')
            timeRuleStatus = "0"
            if ruleName in('DAY', 'WEEK', 'MONTH', 'ODDDAY', 'EVENDAY', 'LASTDAY', 'FIRSTDAY', 'WORKDAY'):
                timeRuleStatus = Producer.compareTimeRule(self, executeDay, ruleName)
            if ruleName == 'HOUR':
               hour = "00"
               realhour = "00"
            seconds = int(hour) * 3600 + int(minute) * 60 + int(second)  ## 配置时间 ##
            realseconds = int(realhour) * 3600 + int(realminute) * 60 + int(realsecond)  ## 当前时间 ##
            if seconds <= realseconds and timeRuleStatus == "0":
                return "0"
            elif seconds <= realseconds and timeRuleStatus == "-1":  ## 本天不需要跑 ##
                return "-1"
            else:
                return "-99999"
        except:
            errors = traceback.format_exc()
            print('Producer[compareTimes] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

    ### 删除已经执行ok任务属性 ###
    def deleteJobId(self):
        try:
            for i in range(self.successQueue.qsize()): ### 获取已经执行任务的队列 ###
                jobId = self.successQueue.get()        ### 获取已经任务Id  jobId ###
                self.taskStatusDist[jobId] = 2         ### jobId 状态成功 ###
                if jobId in bigdog.JOBRELATIONDICT.keys(): ### 判断该JobId是否在 被别人依赖 ###
                    deleteList = bigdog.JOBRELATIONDICT[jobId]  ### 获取被别人依赖的列表 ###
                    for i in deleteList:
                        if i in self.jobRelationDict.keys(): ### key 是否存在 ###
                            tmpList = self.jobRelationDict[i] ### 任务 依赖列表 ###
                            tmpList.remove(jobId)             ### 从依赖列表中删除 已执行任务Id ###
                            self.jobRelationDict[i] = tmpList ### 属性兑换 ###
                        else:
                            pass
                else:
                    pass;### 无底下任务 ###
        except:
            errors = traceback.format_exc()
            print('Producer[deleteJobId] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

    ### 写日志 ###
    def setJobLogStatus(self, key, crontabTime, jobStatus, jobErrorStatus):
        try:
            jobLog.deleteJobLog(key, 0)
            jobLog.insertJobLog(key, 0, crontabTime, '-')
            jobLog.updateJobLog(key, 0, jobStatus, jobErrorStatus)
        except:
            errors = traceback.format_exc()
            print('Producer[setJobLogStatus] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

    ### 删除已经执行error任务属性 ###
    def deleteFailtJobId(self):
        try:
            for i in range(self.errorQueue.qsize()): ### 获取已经执行任务的队列 ###
                jobId, crontabTime = self.errorQueue.get()
                if jobId in bigdog.JOBRELATIONDICT.keys():### 获取向下依赖 jobid ###
                    deleteList = bigdog.JOBRELATIONDICT[jobId] ### 向下依赖列表 ###
                    for key in deleteList:
                        self.errorQueue.put((key, crontabTime))
                        if key in self.jobRelationDict.keys(): ### 依赖 列表 ###
                            if key in self.jobRelationDict.keys():
                                self.jobRelationDict.pop(key)
                            else:
                                pass
                            Producer.setJobLogStatus(self, key, crontabTime, '3', '-99999')
                        else:
                            pass
                else:
                    print('fffxxxx------->' + str(jobId))
            if self.errorQueue.qsize() != 0:
                Producer.deleteFailtJobId(self)
            else:
                pass
        except:
            errors = traceback.format_exc()
            print('Producer[deleteFailtJobId] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

    def run(self):
        try:
            while True:
                Producer.deleteJobId(self) ### 删除已经执行ok队列信息 ###
                Producer.deleteFailtJobId(self) ### 删除已经执行error队列信息 ###
                if len(dict(self.jobRelationDict)) == 0: ### 字典为空 说明该批次任务结束 ###
                    if self.producerOver.qsize() > 0:
                        return "0"
                    else:
                        pass
                for key, value in (self.jobRelationDict).items(): ### 判断任务能够执行 ###
                    if len(value) == 0: ### 能够执行任务 ###
                        print(key)
                        #### statusId 1 开始 2 正常 3 错误 4 未执行
                        jobName, jobPath, executeTime, executeDay, retryCount, ruleName, mailList, statusId = bigdog.JOBINFODICT[key]
                        status = Producer.compareTimes(self, executeTime, ruleName, executeDay)
                        if status == "0":
                            if statusId in(1, 3, 4):### 该任务可以执行 ###
                                self.queue.put(key)                   ### 插入队列中    ###
                                self.jobRelationDict.pop(key)         ### 删除 字典 key ###
                            else:### 该任务在该批次已经执行过并且正常 ###
                                self.jobRelationDict.pop(key)         ### 删除 字典 key ###
                                self.successQueue.put(key)          ### 放入成功队列中 ###
                        elif status == "-1": ### 本天不跑 状态成功 未执行[-99999] ###
                            Producer.setJobLogStatus(self, key, baseModel.getTimeFormat(time.time(), forMat='%Y%m%d%H%M%S'), '2', '-99999')
                            self.jobRelationDict.pop(key)         ### 删除 字典 key ###
                            self.successQueue.put(key)          ### 放入成功队列中 ###
                        else:
                            pass
                    else:
                        pass
                time.sleep(5) ### 每5秒扫描 任务是否执行完成 ###
                print('Producer----> runing|' + str(len(dict(self.jobRelationDict))))
            print('Producer----> over')
        except:
            errors = traceback.format_exc()
            print('Producer[run] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

