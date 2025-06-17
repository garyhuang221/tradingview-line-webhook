from flask import Flask, request
import requests
import os

app = Flask(__name__)

LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")

@app.route('/')
def index():
    return 'TradingView LINE Webhook server is running.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("收到TradingView訊號：", data)

    message_text = f"""📊 交易訊號通知
股票: {data.get('symbol')}
價格: {data.get('price')}
動作: {data.get('action')}
備註: {data.get('note')}
"""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }

    payload = {
        'to': LINE_USER_ID,
        'messages': [{
            'type': 'text',
            'text': message_text
        }]
    }

    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=payload)
    print(response.text)

    return 'OK'

if __name__ == '__main__':
    app.run(port=5000)
