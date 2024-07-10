import requests
import time
import json
from datetime import datetime, timedelta

# 定义API端点和用户信息
username = "yc13884935"
api_url = "https://api.f2pool.com/v2/hash_rate/info"
api_token = "jb10a1qppxectuaty7txfvlsewyg7uhqqbtsnsgs8e0ixwgk728ma9y70gzz6fge"
dingding_webhook = "https://oapi.dingtalk.com/robot/send?access_token=e7e12064d580bf28711608d9103bd48ff77410bea3e57f9fbfff5c754070a3c5"

def fetch_mining_status():
    headers = {
        "Content-Type": "application/json",
        "F2P-API-SECRET": api_token
    }
    payload = {
        "currency": "aleo-staging",
        "user_name": username
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        print("API 响应数据:", data)  # 打印API响应数据
        info = data.get('info', {})
        return {
            "username": username,
            "hashrate": info.get('hash_rate', '无'),
            "h1_hashrate": info.get('h1_hash_rate', '无'),
            "h24_hashrate": info.get('h24_hash_rate', '无'),
            "h1_stale_hashrate": info.get('h1_stale_hash_rate', '无'),
            "h24_stale_hashrate": info.get('h24_stale_hash_rate', '无'),
            "unpaid_rewards": data.get('unpaid_rewards', '无')  # 假设未支付收益在info中
        }
    else:
        print("API 请求失败，状态码:", response.status_code)
        print("API 响应内容:", response.text)  # 打印API响应内容
        return None

def send_to_dingding(message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": "算力"+message
        }
    }
    response = requests.post(dingding_webhook, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败，状态码:", response.status_code)

def time_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return (next_hour - now).total_seconds()

while True:
    status = fetch_mining_status()
    if status:
        message = (
            f"状态:\n"
            f"用户名: {status['username']}\n"
            f"算力: {status['hashrate']}\n"
            f"最近1小时算力: {status['h1_hashrate']}\n"
            f"最近24小时算力: {status['h24_hashrate']}\n"
            f"最近1小时失效算力: {status['h1_stale_hashrate']}\n"
            f"最近24小时失效算力: {status['h24_stale_hashrate']}\n"
            f"未支付收益: {status['unpaid_rewards']}"
        )
        send_to_dingding(message)
        print(message)
    else:
        print("获取数据失败。")

    # 计算距离下一个整点的时间并睡眠
    sleep_time = time_until_next_hour()
    print(f"距离下一个整点还有 {sleep_time / 60:.2f} 分钟")
    time.sleep(sleep_time)