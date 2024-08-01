import random
from datetime import datetime, timedelta

from app.constant.log import URL_PATH_NOT_AUTHEN


# Generate random 6 digits to create code
def generate_code():
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return otp

def convert_date(data):
    for item in data:
        item["due_date"] = item["due_date"].date().isoformat() if item["due_date"] else None
        item["created_date"] = item["created_date"].date().isoformat() if item["created_date"] else None
        # Xử lý giá trị null
        item["payment_date"] = None if item["payment_date"] is None else item["payment_date"].date().isoformat()
    
    return data

def is_path_not_check_authentication(url: str)->bool:
    return URL_PATH_NOT_AUTHEN.get(url, False)
def convert_utc_to_local_time(time: datetime):
    utc_datetime = datetime.utcfromtimestamp(time)

        # Add a timezone offset of +7 hours
    timezone_offset = timedelta(hours=7)
    local_datetime = utc_datetime + timezone_offset
    return local_datetime