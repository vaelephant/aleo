import requests
import json
import logging
from datetime import datetime, timedelta

# 设置日志配置
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('f2pool-a-power.log')
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# 定义API端点和用户信息
username = "yc13884935"
api_url_template = "https://api.f2pool.com/aleo-staging/{username}/{miner}"
api_token = "jb10a1qppxectuaty7txfvlsewyg7uhqqbtsnsgs8e0ixwgk728ma9y70gzz6fge"
dingding_webhook = "https://oapi.dingtalk.com/robot/send?access_token=e7e12064d580bf28711608d9103bd48ff77410bea3e57f9fbfff5c754070a3c5"
miners = ["2230901", "2330901", "2730901", "2830901", "3630801"]

def fetch_mining_status(miner):
    api_url = api_url_template.format(username=username, miner=miner)
    headers = {
        "Content-Type": "application/json",
        "F2P-API-SECRET": api_token
    }
    logger.info(f"Sending request to API for miner {miner}...")
    response = requests.get(api_url, headers=headers)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text: {response.text}")
    if response.status_code == 200:
        data = response.json()
        logger.info(f"API 响应数据: {data}")
        hashrate_history = data.get('hashrate_history', {})
        if hashrate_history:
            latest_timestamp = max(hashrate_history.keys())
            latest_hashrate = hashrate_history[latest_timestamp]
            return {
                "miner": miner,
                "timestamp": latest_timestamp,
                "latest_hashrate": latest_hashrate
            }
        else:
            return None
    else:
        logger.error(f"API 请求失败，状态码: {response.status_code}")
        logger.error(f"API 响应内容: {response.text}")
        return None

def send_to_dingding(message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    logger.info("Sending message to Dingding...")
    response = requests.post(dingding_webhook, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        logger.info("消息发送成功")
    else:
        logger.error(f"消息发送失败，状态码: {response.status_code}")

print("开始运行脚本...")
logger.info("开始运行脚本...")

messages = []
for miner in miners:
    logger.info(f"Fetching mining status for miner {miner}...")
    status = fetch_mining_status(miner)
    if status:
        message = (
            f"workid: {status['miner']}\n"
            f"时间戳: {status['timestamp']}\n"
            f"最新算力: {status['latest_hashrate']}\n"
        )
        messages.append(message)
        logger.info(message)
    else:
        logger.error(f"获取矿工 {miner} 数据失败。")

if messages:
    full_message = "算力信息:\n" + "\n".join(messages)
    send_to_dingding(full_message)
    logger.info(full_message)
    print(full_message)
else:
    logger.error("未能获取到任何矿工的数据。")