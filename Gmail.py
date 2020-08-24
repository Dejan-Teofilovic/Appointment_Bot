# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 17:49:07 2020

@author: Amir
"""


import email
import imaplib
from email.header import decode_header
import re

def gmail_ckeck(email_address, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    (retcode, capabilities) = mail.login(email_address,password)
    mail.list()
    mail.select('inbox')

    flag = False
    while 1:
        opt_list = []
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        (retcode, capabilities) = mail.login(email_address, password)
        mail.list()
        mail.select('inbox')            
        status, messages = mail.search(None, '(UNSEEN)')
        if messages[0].decode("utf-8") == '':
            flag = False
        else:
            res = messages[0].decode("utf-8")
            messages = res.split(' ')
            for i in range(len(messages)):
                typ, data = mail.fetch(messages[i],'(RFC822)')
                
                for response in data:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        
                        if isinstance(subject, bytes):
                            subject = subject.decode()
                            
                        if subject == 'One-time Password (OTP) Confirmation Email':
                            flag = True
                            if msg.is_multipart():
                                for part in msg.walk():   # iterate over email parts
                                    # extract content type of email
                                    content_type = part.get_content_type()
                                    try:
                                        # get the email body
                                        body = part.get_payload(decode=True).decode()
                                    except:
                                        pass
                                    if content_type == "text/plain":
                                        opt = re.findall(r'(\d{6})', body)
                                        opt_list.append(opt)
                            else:
                                content_type = msg.get_content_type()    # extract content type of email
                                body = msg.get_payload(decode=True).decode()
                                if content_type == "text/plain":
                                    opt = re.findall(r'(\d{6})', body)
                                    opt_list.append(opt)
                    
        if flag:
            
            break
        else:
            pass
    
    mail.logout()   
    return opt_list[-1]            








