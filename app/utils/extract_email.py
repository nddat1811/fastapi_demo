from smtplib import SMTP
import dns.resolver
import dns.exception
import socket
import socks  # PySocks
import re
from call_function_with_timeout import SetTimeout
import pandas as pd
import numpy as np
from fastapi import HTTPException,status
import logging
# sử dụng proxy để gửi nhiều nhiều request mà không bị chặn

class TestFailed(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class SocksSMTP(SMTP):

    def __init__(self,
                host='',
                port=0,
                local_hostname=None,
                timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                source_address=None,
                proxy_type=None,
                proxy_addr=None,
                proxy_port=None,
                proxy_rdns=True,
                proxy_username=None,
                proxy_password=None,
                socket_options=None):

        self.proxy_type = proxy_type
        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
        self.proxy_rdns = proxy_rdns
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.socket_options = socket_options
        if self.proxy_type:
            self._get_socket = self.socks_get_socket
        super(SocksSMTP, self).__init__(host, port,
                                        local_hostname, timeout, source_address)

    def socks_get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socks.create_connection((host, port),
                                        timeout=timeout,
                                        source_address=self.source_address,
                                        proxy_type=self.proxy_type,
                                        proxy_addr=self.proxy_addr,
                                        proxy_port=self.proxy_port,
                                        proxy_rdns=self.proxy_rdns,
                                        proxy_username=self.proxy_username,
                                        proxy_password=self.proxy_password,
                                        socket_options=self.socket_options)
def get_mx(domain):
    try:
        if domain is None:
            return None
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        mx_records = resolver.query(domain.strip(), 'MX')
        if not mx_records:
            return None
        mx_records = sorted(mx_records, key=lambda r: r.preference)
        mx_record = str(mx_records[0].exchange)
        return mx_record[0:len(mx_record) - 1]

    except Exception as e:
        # print(f"An error occurred: {e}")
        return None
#can.lt 20/02/2024
def group_email_v2(mailList):
    result = {}
    for row in mailList: 
        domain = row.domain
        if domain in result:
            result[domain]["mailList"].append(row)
        else:
            result[domain] = {"domain": domain, "mailList": [row]}
    return result
#can.lt 20/02/2024
def sub_ping_email_v2(email, smtp):
    target_email = email and email.strip()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, target_email):
        smtp.helo()  # send the HELO command
        smtp.mail('product.mf2@gmail.com')  # send the MAIL command
        resp = smtp.rcpt(target_email)
        return resp[0]
    return -1
def ping_email_v2(email, smtp, config_time):
    ping_email = SetTimeout(sub_ping_email_v2, timeout=config_time)
    is_done, _, _, result = ping_email(email=email, smtp=smtp)
    if is_done == False:
        return -2
    return result
#can.lt 20/02/2024
def cluster_email_v2(
                    domain: str, 
                    email_check_id: int,
                    config_time: int):
    is_error = False
    try:
        mx = get_mx(domain["domain"])
        # if mx is None:
        #     for email in domain["mailList"]:
        #         return is_error
        #         update_email_check_detail(db=db, 
        #                                     email_check_detail_id=email.email_check_detail_id, 
        #                                     mx="", 
        #                                     status=EmailCheckDetailEnum.illegal, 
        #                                     detail="243 -> Không xác định được tên miền",
        #                                     email_check_id=email_check_id)
        #     return is_error
        email_catch_all = "11111111111111999999999pspcns@"+domain["domain"]
        with SocksSMTP(mx) as smtp:
            if ping_email_v2(email=email_catch_all, smtp=smtp, config_time=config_time) == 250:# case catch all
                # for email in domain["mailList"]:
                #     return is_error
                #     update_email_check_detail(db=db, 
                #                             email_check_detail_id=email.email_check_detail_id, 
                #                             mx=mx, 
                #                             status=EmailCheckDetailEnum.unknown, 
                #                             detail="254 -> Email KXĐ",
                #                             email_check_id=email_check_id)
                # return is_error
            # for email in domain["mailList"]:
            #     try:
                status_code = ping_email_v2(email=email.email, smtp=smtp, config_time=config_time)
                if status_code == 250:  # check the status code
                    pass
                    # update_email_check_detail(db=db, 
                    #                   email_check_detail_id=email.email_check_detail_id, 
                    #                   mx=mx, 
                    #                   status=EmailCheckDetailEnum.valid,
                    #                   detail="",
                    #                   email_check_id=email_check_id)
                elif status_code >= 421:# https://www.greenend.org.uk/rjk/tech/smtpreplies.html
                    return is_error
                    update_email_check_detail(db=db, 
                                        email_check_detail_id=email.email_check_detail_id, 
                                        mx=mx, 
                                        status=EmailCheckDetailEnum.illegal, 
                                        detail=f"272 -> Email sai, status code: {status_code}",
                                        email_check_id=email_check_id)
                elif status_code == -1:
                    return is_error
                    update_email_check_detail(db=db, 
                                        email_check_detail_id=email.email_check_detail_id, 
                                        mx=mx, 
                                        status=EmailCheckDetailEnum.illegal, 
                                        detail="279 -> Email không đúng định dạng",
                                        email_check_id=email_check_id)
                elif status_code == -2:
                    return is_error
                    update_email_check_detail(db=db, 
                                        email_check_detail_id=email.email_check_detail_id, 
                                        mx=mx, 
                                        status=EmailCheckDetailEnum.unknown, 
                                        detail="286 -> Lỗi trong quá trình xử lý",
                                        email_check_id=email_check_id)
                    # except Exception as err:
                    #     return is_error
                    #     update_email_check_detail(db=db, 
                    #                         email_check_detail_id=email.email_check_detail_id, 
                    #                         mx=mx, 
                    #                         status=EmailCheckDetailEnum.unknown, 
                    #                         detail=f"293 -> Lỗi trong quá trình xử lý, error: {err}",
                    #                         email_check_id=email_check_id)
    except Exception as err:
        print("dáokadsok")
        try:
            for email in domain["mailList"]:
                if str(err).find("WinError 10060") != -1:
                    return is_error
                    update_email_check_detail(db=db, 
                                    email_check_detail_id=email.email_check_detail_id, 
                                    mx=mx, 
                                    status=EmailCheckDetailEnum.illegal, 
                                    detail=f"303 -> Lỗi trong quá trình xử lý, error: {err}",
                                    email_check_id=email_check_id)
                elif str(err).find("(421, b'4.7.0 Not allowed.')") != -1:
                    return is_error
                    update_email_check_detail(db=db, 
                                    email_check_detail_id=email.email_check_detail_id, 
                                    mx=mx, 
                                    status=EmailCheckDetailEnum.unknown, 
                                    detail=f"310 -> Lỗi trong quá trình xử lý, error: {err}",
                                    email_check_id=email_check_id)
                else:
                    return is_error
                    update_email_check_detail(db=db, 
                                    email_check_detail_id=email.email_check_detail_id, 
                                    mx=mx, 
                                    status=EmailCheckDetailEnum.unknown, 
                                    detail=f"317 -> Lỗi trong quá trình xử lý, error: {err}",
                                    email_check_id=email_check_id)
        except Exception as err:
            #update_email_check(db=db, email_check_id=email_check_id, is_error=True, error_msg=str(err))
            is_error = True
    return is_error
# #can.lt 19/02/2024
# def check_email_exist_v2(email_check_id: int):
#     try:
#         mail_list = get_all_email_check_detail_waiting(db=db, 
#                                                     email_check_id=email_check_id)
#         mail_group = group_email_v2(mail_list)
#         is_error = False
#         for domain in mail_group:
#             config_time = int(get_config(db, code="CONFIG_PING_EMAIL_TIME"))
#             is_error = cluster_email_v2(domain=mail_group[domain],
#                                         db=db,
#                                         email_check_id=email_check_id,
#                                         config_time=config_time)
#             if is_error == True:
#                 break
#         if is_error == False:
#             update_email_check(db=db, 
#                             email_check_id=email_check_id, 
#                             is_complete=True)
#     except Exception as err:
#         update_email_check(db=db, 
#                         email_check_id=email_check_id, 
#                         is_error=True, 
#                         error_msg=str(err))

def check_email_exist_v3(email: str):
    try:
        # Tạo một danh sách email giả để phù hợp với định dạng hiện tại
        mail_list = [{'email': email, 'domain': email.split('@')[1]}]
        mail_group = group_email_v2(mail_list)
        
        is_error = False
        for domain in mail_group:
            config_time = 30#int(get_config(db, code="CONFIG_PING_EMAIL_TIME"))
            print("ex", mail_group[domain])
            is_error = cluster_email_v2(
                domain=mail_group[domain],
                email_check_id=None,  # Không sử dụng email_check_id trong trường hợp này
                config_time=config_time
            )
            if is_error:
                break
        # print ("opasdkoasdkadsopk")
        if not is_error:
            return "ok"
            print("Kiểm tra email hoàn tất mà không có lỗi.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kiểm tra email thất bại")
            print("Đã xảy ra lỗi trong quá trình kiểm tra email.")
        
        return "Ok=ádads"
    except Exception as err:
        print(f"Đã xảy ra lỗi: {err}")