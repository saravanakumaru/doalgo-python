import json
import requests
import time

def send_message_bot(chat_id, text):
    url = 'https://api.telegram.org/bot<YOUR-BOT-TOKEN>/sendMessage'
    r = requests.post(url, {'chat_id': chat_id, 'text': text}).json()
    print(r)

def lambda_handler(event, context):
    # TODO implement

    send_message_bot(-1001308804032, "dont block me.")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
