import random
from datetime import datetime

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