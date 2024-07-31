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
    
    # Check file is already exists, if not create new file
    if not os.path.exists(filename):
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "action_datetime", "path_name", "method", "ip", 
                "status_response", "response", "description", "request_body", 
                "request_query", "duration"
            ])
    
    # write log into csv
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            req.action_datetime.strftime("%Y-%m-%d %H:%M:%S"), 
            req.path_name, req.method, req.ip, req.status_response, req.response, 
            req.description, req.request_body, req.request_query, req.duration
        ])

