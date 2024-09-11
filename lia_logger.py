import os
import datetime

# Project LIA
# LIA LOGGER - MODULE
# LIA 로그를 수집합니다.
# Created : 24.02.22

print("[alert] lia_logger Module Load Complete")

LOG_DIR = "logdata"

def get_log_file_path():
    today_date = datetime.date.today()
    log_file_name = f"logdata_{today_date}.txt"
    log_file_path = os.path.join(LOG_DIR, log_file_name)
    return log_file_path

def logger(sender, log_type, nick_name, data=None, answer_data=None, level_ori=None, level_after=None):
    log_file_path = get_log_file_path()
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] [alert] logger 초기화됨\n")
    if log_type == "levelup":
        with open(log_file_path, "a",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{log_type}] [{sender}({nick_name})]: 레벨업 {level_ori} -> {level_after}\n"
            log_file.write(log_entry)
    elif log_type == "normal":
        with open(log_file_path, "a",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{log_type}] [{sender}({nick_name})]: {data}, [answer]: {answer_data}\n"
            log_file.write(log_entry)
    elif log_type == "nodata":
        with open(log_file_path, "a",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{log_type}] [{sender}({nick_name})]: {data}, [answer]: {answer_data}\n"
            log_file.write(log_entry)
    elif log_type == "reboot":
        with open(log_file_path, "a",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{log_type}] 서버가 재부팅됨\n"
            log_file.write(log_entry)
    elif log_type == "join":
        with open(log_file_path, "a",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{log_type}] LIA가 {sender}서버에 참가했습니다.\n"
            log_file.write(log_entry)
    elif log_type == "leave":
        with open(log_file_path, "a",  encoding='utf-8') as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{log_type}] LIA가 {sender}서버에서 나갔습니다.\n"
            log_file.write(log_entry)        
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)