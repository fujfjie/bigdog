# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import multiprocessing, traceback, time, os, threading, random, baseModel, jobLog, metaInfo, bigdog
class Consumer(multiprocessing.Process):
    def __init__(self, tmpStartJobRelation, workQueue, productName, vDate, vSnapshot, successQueue, errorQueue, parallelNums, producerOver):
        multiprocessing.Process.__init__(self)
        self.jobRelationDict = tmpStartJobRelation
        self.queue = workQueue
        self.productName = productName
        self.vDate = vDate
        self.vSnapshot = vSnapshot
        self.successQueue = successQueue
        self.errorQueue = errorQueue
        self.parallelNums = parallelNums
        self.producerOver = producerOver

    def deleteJobId(self, jobId): ### 将已经执行 ok任务放到 删除队列中 ###
        try:  ### JOBINFODICT   STARTJOBRELATIONDICT   JOBRELATIONDICT
            self.successQueue.put(jobId)
        except:
            errors = traceback.format_exc()
            print('Consumer[deleteJobId] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

    def deleteFailtJobId(self, jobId, crontabTime): ### 将已经执行 fail任务 放到 异常队列中 ###
        try:
            self.errorQueue.put((jobId, crontabTime))
        except:
            errors = traceback.format_exc()
            print('Consumer[deleteFailtJobId] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"

    def runJob(self, jobId):
        try:
            #### statusId 1 开始 2 正常 3 错误 4 未执行
            jobName, jobPath, executeTime, executeDay, retryCount, ruleName, mailList, statusId = bigdog.JOBINFODICT[jobId]
            if mailList is None:
                mailList = bigdog.GROUPINFO[-1]
            crontabTime = baseModel.getTimeFormat(time.time(), forMat='%Y%m%d%H%M%S')
            alarmIndex = 0
            if retryCount is None:
                retryCount = bigdog.GROUPINFO[2]
            for i in range(retryCount):  ### 异常后 重复多少次 ###
                ### 执行程序 ###
                tmpLogName = jobPath.split('/')[-1][0:-2] + 'log.' + self.vSnapshot
                tmpLogPathName = metaInfo.LOGDIRPATH + '/' + metaInfo.getvDate() + '/' + metaInfo.getvGroupId() + '/' + tmpLogName + '.' + str(i)
                baseModel.rmFile(tmpLogPathName)
                jobLog.deleteJobLog(jobId, i)
                jobLog.insertJobLog(jobId, i, crontabTime, tmpLogPathName)
                baseCmd = 'bash ' + jobPath + ' ' + self.vDate + ' ' + mailList + ' ' + self.vSnapshot + ' ' + tmpLogPathName + ' >>' + tmpLogPathName + ' 1>>' + tmpLogPathName + ' 2>>' + tmpLogPathName
                print(baseCmd)
                status = os.system(baseCmd)
                if status == 0:
                    ### 调整日志 ###
                    jobLog.updateJobLog(jobId, i, 2, status)
                    ### 删除 执行成功 jobid ###
                    Consumer.deleteJobId(self, jobId)
                    break
                else:
                    jobLog.updateJobLog(jobId, i, 3, status)
                alarmIndex = i
                ### 是否Hive hive 日志解析###
            if alarmIndex == retryCount - 1:  ### 重复次数都错误 告警###
                msgContent = 'bigdog[' + self.vDate + ':' + self.vSnapshot + ']{' + bigdog.GROUPINFO[0] + '---' + jobPath + ' is execution error}-->' + tmpLogPathName
                baseModel.sendMsgInfo(metaInfo.taskSubject, mailList, msgContent)
                ### 依赖相关程序 下线 ###
                Consumer.deleteFailtJobId(self, jobId, crontabTime)
            else:
                pass;#print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx------->' + str(jobId))
        except:
            errors = traceback.format_exc()
            print('Consumer[runJob] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"
    def run(self):
        try:
            while True:
                print('C---->' + str(self.jobRelationDict))
                time.sleep(5) ### 每5秒扫描 查看队列是否完成 ###
                threadNums = threading.activeCount()
                workQueueSize = self.queue.qsize()
                jobSize = len(self.jobRelationDict)
                if jobSize == 0 and workQueueSize == 0:
                    tmpi = 0
                    for tmpthreadname in threading.enumerate(): ### 获取所有队列 ###
                        if (tmpthreadname.name)[:14] == 'bigDogJobList-':  ### 判断是否存在 运行线程 ###
                            tmpi += 1
                    if tmpi == 0:
                        self.producerOver.put('ok')
                        return "0"
                    else:
                        pass;
                else:
                    if threadNums >= self.parallelNums + 2: ### 线程数 超过阀值 ###
                        pass
                    else:
                        if (self.parallelNums + 2) - threadNums > workQueueSize:
                            executeSize = workQueueSize
                        else:
                            executeSize = self.parallelNums + 2 - threadNums
                        for threadTmp in range(executeSize):
                            jobId = self.queue.get()
                            tmpThread = threading.Thread(target=Consumer.runJob, args=(self, jobId), name='bigDogJobList-' + str(random.randint(1,1000000000000)))
                            tmpThread.start()
            print('Consumer----> over')
        except:
            errors = traceback.format_exc()
            print('Consumer[run] ->' + errors)
            baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
            return "-99999"


