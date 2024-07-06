import time
import re
from datetime import datetime, timedelta

log_file_path = 'aleo.log'
workerid = '02'

def monitor_log_file(log_file_path):
    print("Monitoring Aleo log file for performance metrics...")
    
    while True:
        last_perf_line = None
        with open(log_file_path, 'r') as file:
            lines = file.readlines()[-100:]  # 读取最后100行
        for line in lines:
            if 'perf' in line:
                last_perf_line = line.strip()
        if last_perf_line:
            display_perf_data(last_perf_line)
        else:
            print("No 'perf' keyword found in the last 100 lines.")
        time.sleep(3)  # 每3秒查询一次

def display_perf_data(line):
    # 提取时间戳和1m后的数字
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?1m: ([\d.]+) P/s')
    match = pattern.search(line)
    if match:
        timestamp = match.group(1)
        one_min_perf = match.group(2)
        log_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.now()
        if current_time - log_time > timedelta(hours=1):
            print("Error: Last 'perf' entry is older than 1 hour.")
        else:
            print(f"{workerid}:{timestamp} - powers: {one_min_perf} P/s")
    else:
        # 增加调试信息，显示未能匹配的行
        print(f"Pattern not matched in line: {line}")

if __name__ == "__main__":
    monitor_log_file(log_file_path)