'''
使用说明：

1、将该程序放在和aleo.log同目录下
2、注意用3秒做轮询测试，成功后修改成3600秒
3、注意修改workerid

'''

import time
import re
import json
import requests
from datetime import datetime, timedelta

log_file_path = 'aleo.log'   # 日志文件
workerid = '02'              # 机器ip最后数字
sleeptime = 3            # 多久查询一次，我们设定为一小时：3600秒
dingtalk_webhook_ok = 'https://oapi.dingtalk.com/robot/send?access_token=0602e9fb26e9f44019b76a8d517b0d61bc3def4648ec528ed1d426e21f93ccf2'  # 替换为你的钉钉机器人Webhook URL
dingtalk_webhook_error = 'https://oapi.dingtalk.com/robot/send?access_token=33b8bb7fbfa87f1eefabf5c02451871bae05b080cc8b6fb7b441e126d038d149'  # ��换为你的����机器人Webhook URL =
def send_to_dingtalk_Ok(message):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": '[算力]'+message
        }
    }
    response = requests.post(dingtalk_webhook_ok, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Failed to send message to DingTalk: {response.text}")

def send_to_dingtalk_error(message):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": '[报警]'+message
        }
    }
    response = requests.post(dingtalk_webhook_error, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Failed to send message to DingTalk: {response.text}")



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
        time.sleep(sleeptime)  # 每隔设定的时间查询一次

def display_perf_data(line):
    # 提取时间戳和1m后的数字
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?1m: ([\d.]+) P/s')
    match = pattern.search(line)
    if not match:
        # 尝试不同格式的时间戳
        pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{1}:\d{2}:\d{2}\.\d{3}).*?1m: ([\d.]+) P/s')
        match = pattern.search(line)
    if match:
        timestamp = match.group(1)
        one_min_perf = match.group(2)
        log_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.now()
        if current_time - log_time > timedelta(hours=1):
            # 钉钉报警
            message = f"Error: Last 'perf' entry is older than 1 hour. WorkerID: {workerid}"
            print(message)
            send_to_dingtalk_error(message)
        else:
            # 钉钉播报
            message = f"{workerid}:{timestamp} - powers: {one_min_perf} P/s"
            print(message)
            send_to_dingtalk_Ok(message)
    else:
        # 增加调试信息，显示未能匹配的行
        print(f"Pattern not matched in line: {line}")

if __name__ == "__main__":
    monitor_log_file(log_file_path)