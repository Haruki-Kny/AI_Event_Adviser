import os
import subprocess
from fastapi import FastAPI, Request
import openai
from linebot import WebhookParser, LineBotApi
from linebot.models import TextSendMessage

# 参考サイト：https://qiita.com/IoriGunji/items/d84fd35e0da1b68ff7f5#python-%E3%82%B3%E3%83%BC%E3%83%89%E3%81%AE%E4%BD%9C%E6%88%90

# 環境変数の取得
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
LINE_CHANNEL_ACCESS_TOKEN = os.environ['EVENT_ADVISER_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['EVENT_ADVISER_SECRET']
OPENAI_CHARACTER_PROFILE = '''
テスト
'''


openai.api_key = OPENAI_API_KEY
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_parser = WebhookParser(LINE_CHANNEL_SECRET)
app = FastAPI()


@app.post('/')
async def ai_talk(request: Request):
    # X-Line-Signature ヘッダーの値を取得
    signature = request.headers.get('X-Line-Signature', '')

    # request body から event オブジェクトを取得
    events = line_parser.parse((await request.body()).decode('utf-8'), signature)

    # 各イベントの処理（※1つの Webhook に複数の Webhook イベントオブジェっｚクトが含まれる場合あるため）
    for event in events:
        if event.type != 'message':
            continue
        if event.message.type != 'text':
            continue

        # LINE パラメータの取得
        line_user_id = event.source.user_id
        line_message = event.message.text

        # ChatGPT からトークデータを取得
        # response = openai.ChatCompletion.create(
        #     model = 'gpt-3.5-turbo'
        #     , temperature = 0.5
        #     , messages = [
        #         {
        #             'role': 'system'
        #             , 'content': OPENAI_CHARACTER_PROFILE.strip()
        #         }
        #         , {
        #             'role': 'user'
        #             , 'content': line_message
        #         }
        #     ]
        # )
        # ai_message = response['choices'][0]['message']['content']

        # # LINE メッセージの送信
        # line_bot_api.push_message(line_user_id, TextSendMessage(ai_message))
        line_bot_api.push_message(line_user_id, TextSendMessage('オウム返し\n' + line_message))


    # LINE Webhook サーバーへ HTTP レスポンスを返す
    return 'ok'
