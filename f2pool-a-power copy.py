import requests
import time
import json
import logging
from datetime import datetime, timedelta

# 设置日志配置
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个文件处理器
file_handler = logging.FileHandler('f2pool-a-power.log')
file_handler.setLevel(logging.INFO)

# 创建一个流处理器（输出到终端）
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# 创建一个格式化器并将其添加到处理器中
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 将处理器添加到日志记录器中
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

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
    logger.info("Sending request to API...")
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        logger.info(f"API 响应数据: {data}")  # 打印API响应数据
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
        logger.error(f"API 请求失败，状态码: {response.status_code}")
        logger.error(f"API 响应内容: {response.text}")  # 打印API响应内容
        return None

def send_to_dingding(message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": "算力" + message
        }
    }
    logger.info("Sending message to Dingding...")
    response = requests.post(dingding_webhook, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        logger.info("消息发送成功")
    else:
        logger.error(f"消息发送失败，状态码: {response.status_code}")

def time_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return (next_hour - now).total_seconds()

print("开始运行脚本...")
logger.info("开始运行脚本...")

logger.info("Fetching mining status...")
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
    #send_to_dingding(message)
    logger.info(message)
else:
    logger.error("获取数据失败。")