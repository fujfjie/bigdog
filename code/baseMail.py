# -*- coding: utf-8 -*-
"""
    :version: V1.1.1.2016/5/24_beta
    :author: fisher.jie
    :file: dbConnect.py
    :time: 2017/03/13
"""
import smtplib, traceback, metaInfo, baseModel
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.text import MIMEText

def getAttFileContent(attFilePath):
    try:
        att = MIMEText(open(attFilePath, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="' + attFilePath.split('/')[-1] + '"'
        return att
    except:
        errors = traceback.format_exc()
        print('baseMail[getAttFileContent] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"

def sendMail(subject, sendMail, textContent = None, htmlContent = None, attFilePath = None):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        if textContent is not None:
            text = textContent
            part1 = MIMEText(text, 'plain')
            msg.attach(part1)
        if htmlContent is not None:
            html = htmlContent
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
        msg['From'] = formataddr([metaInfo.getmailUserHead(), metaInfo.getmailUser()])
        if attFilePath is not None:
            att = getAttFileContent(attFilePath)
            msg.attach(att)
        smtp = smtplib.SMTP()
        smtp.connect(metaInfo.getmailHost(), metaInfo.getmailPort())
        smtp.login(metaInfo.getmailUser(), metaInfo.getmailUserPassWord())
        smtp.sendmail(metaInfo.getmailUser(), sendMail.split(','), msg.as_string())
        smtp.quit()
        return "0"
    except:
        errors = traceback.format_exc()
        print('baseMail[sendMail] ->' + errors)
        baseModel.setWriteContentList(metaInfo.getvLogFilePath(), errors, 'a')
        return "-99999"
