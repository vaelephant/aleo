import subprocess
import time
import random
import requests
import json

workid = '02'
base_variable_part = 'yc13884935.02-3090*1'

def send_dingtalk_message(message):
    url = "https://oapi.dingtalk.com/robot/send?access_token=46cadf10343c8f951440686dfd2baf4e10e0ad5f7231418daebc8c9c64f58ada"
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

def restart_command():
    while True:
        variable_part = base_variable_part
        command = f"nohup ./aleo-miner -u 192.168.0.136:1080 -w {variable_part} -d 0 >>aleo.log 2>&1 &"
        
        # 使用subprocess启动命令
        process = subprocess.Popen(command, shell=True)
        
        # 发送钉钉消息通知
        send_dingtalk_message(f"id={workid},重启命令已启动: {command}")
        
        # 等待1小时（3600秒）
        time.sleep(3600)
        
        # 杀死进程
        subprocess.Popen("pkill -f 'aleo-miner'", shell=True)
        
        # 发送钉钉消息通知
        #send_dingtalk_message("id={workid},进程已终止，准备重启命令")

if __name__ == "__main__":
    restart_command()