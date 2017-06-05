# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import sys, time, bigdog, Producer, Consumer, multiprocessing, traceback, jobLog, baseModel, metaInfo
def getSysInfo():
    import metaInfo
    ### 获取当前快照 ###  vDate, productName
    vSnapshot = baseModel.getTimeFormat(time.time(), forMat='%Y%m%d%H%M%S')
    if len(sys.argv) == 3:
        vDate, vGroupId = sys.argv[1:]
    elif len(sys.argv) == 4:  ## 按照批次来执行 ## 上一个批次出现异常，可以按照该批次进行执行【重跑】 ##
        vDate, vGroupId, vSnapshot = sys.argv[1:]
    elif len(sys.argv) == 5:
        vDate, vGroupId, vSnapshot, vJobId = sys.argv[1:]
        if vSnapshot == 'jobId':
            vSnapshot = baseModel.getTimeFormat(time.time(), forMat='%Y%m%d%H%M%S')
        metaInfo.setvJobId(vJobId)
    metaInfo.setvDate(vDate)
    metaInfo.setvGroupId(vGroupId)
    metaInfo.setvSnapshot(vSnapshot)
    vLogFilePath = metaInfo.LOGDIRPATH + '/' + vDate + '/' + vGroupId + '/program.' + vGroupId + '.' + vSnapshot + '.log'
    metaInfo.setvLogFilePath(vLogFilePath)

def getPushMail():
    import metaInfo
    metaInfo.setmailHost(bigdog.PUSHMAIL[0])
    metaInfo.setmailUser(bigdog.PUSHMAIL[1])
    metaInfo.setmailUserHead(bigdog.PUSHMAIL[2])
    metaInfo.setmailUserPassWord(bigdog.PUSHMAIL[3])
    metaInfo.setmailPort(bigdog.PUSHMAIL[4])
    metaInfo.settaskSubject(bigdog.PUSHMAIL[5])

### 工作队列 ###
workQueue = multiprocessing.Queue()
### 删除任务队列 ###
successQueue = multiprocessing.Queue()
### 删除任务队列 ###
errorQueue = multiprocessing.Queue()
### 生产结束 状态位 ###
producerOver = multiprocessing.Queue()
def run():
    try:
        #print(bigdog.STARTJOBRELATIONDICT)
        if len(bigdog.STARTJOBRELATIONDICT) > 0:
            manager = multiprocessing.Manager()
            tmpStartJobRelation = manager.dict(bigdog.STARTJOBRELATIONDICT)
            jobLog.deleteGroupLog()
            jobLog.insertGroupLog()
            producer = Producer.Producer(tmpStartJobRelation, workQueue, metaInfo.getvGroupId(), metaInfo.getvDate(), metaInfo.getvSnapshot(), successQueue, errorQueue, {}, producerOver) ### 生产者 ###
            consumer = Consumer.Consumer(tmpStartJobRelation, workQueue, metaInfo.getvGroupId(), metaInfo.getvDate(), metaInfo.getvSnapshot(), successQueue, errorQueue, int(bigdog.GROUPINFO[1]), producerOver) ### 消费者 ###
            producer.start()
            consumer.start()
            consumer.join()
            producer.join()
            #jobLog.updateGroupLog(0)
            ### 运行统计信息 ##
            groupRunInfo = jobLog.getGroupRunInfo()
            #print(tmpStatus)
            if isinstance(groupRunInfo, tuple):
               confPv, relaPv, succPv, errPv = groupRunInfo
               if errPv == 0:
                   jobLog.updateGroupLog(2, confPv, relaPv, succPv, errPv)
               else:
                   jobLog.updateGroupLog(3, confPv, relaPv, succPv, errPv)
               msgContents = 'bigdog[' + metaInfo.getvGroupId() + ':%s:%s]{confPv:%d,relaPv:%d,succPv:%d,errPv:%d}'
               msgContents = msgContents % (metaInfo.getvDate(), metaInfo.getvSnapshot(), confPv, relaPv, succPv, errPv)
               print(msgContents)
               baseModel.sendMsgInfo('bigdog group[' + metaInfo.getvGroupId() + '] run status', bigdog.GROUPINFO[-1], msgContents)
            else:
               pass
        else:
            print('配置信息有问题')
    except:
        errors = traceback.format_exc()
        print('mainInfo[run] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"
def main():
    getSysInfo()
    ### 初始化 文件夹与 调度信息 ###
    bigdog.initStart()
    getPushMail()
    run()

main()
