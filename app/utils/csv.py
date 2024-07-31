import csv
import os
from datetime import datetime, timedelta

from app.db.db_log import LogModel

def get_week_number(date):
    return date.isocalendar()[1]

def get_csv_filename(date):
    week_number = get_week_number(date)
    year = date.year
    return f"log_week_{year}_{week_number}.csv"

def write_log_csv(req: LogModel):
    today = datetime.now()
    filename = get_csv_filename(today)
    
    # Kiểm tra nếu file không tồn tại, tạo mới và ghi header
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "action_datetime", "path_name", "method", "ip", 
                "status_response", "response", "description", "request_body", 
                "request_query", "duration"
            ])
    
    # Ghi log vào file CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            req.action_datetime.strftime("%Y-%m-%d %H:%M:%S"), 
            req.path_name, req.method, req.ip, req.status_response, req.response, 
            req.description, req.request_body, req.request_query, req.duration
        ])

# Ví dụ ghi log
