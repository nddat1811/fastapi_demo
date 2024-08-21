from smtplib import SMTP
import re
import dns.resolver
from call_function_with_timeout import SetTimeout
import socket
from fastapi import HTTPException, status
import socks  # PySocks


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
    
# Các hàm phụ trợ
def get_mx(domain):
    try:
        if domain is None:
            return None
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        mx_records = resolver.resolve(domain.strip(), 'MX')
        if not mx_records:
            return None
        mx_records = sorted(mx_records, key=lambda r: r.preference)
        mx_record = str(mx_records[0].exchange)
        print("OKOKO: ", mx_record[:-1])
        return mx_record[:-1]  # Loại bỏ dấu chấm cuối cùng

    except Exception as e:
        return None

def sub_ping_email_v2(email, smtp):
    target_email = email.strip()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, target_email):
        smtp.helo()
        smtp.mail('product.mf2@gmail.com')
        resp = smtp.rcpt(target_email)
        return resp[0]
    return -1

def ping_email_v2(email, smtp, timeout):
    ping_email = SetTimeout(sub_ping_email_v2, timeout=timeout)
    is_done, _, _, result = ping_email(email=email, smtp=smtp)
    if not is_done:
        return -2
    return result

async def check_email_exist_v2(email: str):
    try:
        # Tách miền từ email
        domain = email.split('@')[1]
        mx = get_mx(domain)
        if mx is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không xác định được tên miền")
        
        email_catch_all = "11111111111111999999999pspcns@" + domain
        # mx = "gmail-smtp-in.l.google.com"
        # print("mk: ", mx)
        with SocksSMTP(host=mx) as smtp:
            # Kiểm tra địa chỉ email catch-all
            if ping_email_v2(email=email_catch_all, smtp=smtp, timeout=10) == 250:
                print(f"Email {email} có thể là hợp lệ.")
                return
            
            # Kiểm tra địa chỉ email cụ thể
            status_code = ping_email_v2(email=email, smtp=smtp, timeout=30)
            if status_code == 250:
                return True
            elif status_code >= 421:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email {email}, không hợp lệ")
            elif status_code == -1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email {email}, không đúng định dạng.")
            elif status_code == -2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Đã xảy ra lỗi trong quá trình kiểm tra email {email}.")
                
            return "not oke"
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Đã xảy ra lỗi trong quá trình kiểm tra email {str(err)}.")
