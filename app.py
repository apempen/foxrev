import os, random
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    LocationMessage,
    TextMessage,
    TextSendMessage,
    FollowEvent,
    StickerSendMessage,
    VideoSendMessage,
    AudioSendMessage,
    LocationSendMessage,
    ImageSendMessage,
    QuickReplyButton,
    QuickReply,
    CameraRollAction,
    CameraAction,
    LocationAction
)
import time
import handle_sql
from janken import handle_janken

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    user_id = event.source.user_id
    line_bot_api.push_message(user_id, TextSendMessage(text="報告感謝だこん！🦊🦊🦊"))
    result = handle_sql.getLastReportTime(user_id)
    crr_time = time.time()
    lasttime = 0.0
    for row in result:
        lasttime = row[0]
    if(crr_time - lasttime >= 10):
        handle_sql.add("キツネ", event.message.latitude, event.message.longitude, user_id) 
        BroadcastMsg("目撃情報があるこん！")

    latest_data = handle_sql.getLatestData(3)
    if(latest_data[2]):
        if(crr_time - latest_data[2][0] <= 10 * 60):
            latitude = (latest_data[0][2] + latest_data[0][2] + latest_data[0][2]) / 3
            longitude = (latest_data[0][3] + latest_data[0][3] + latest_data[0][3]) / 3
            BroadcastMsg(
                "10分以内に目撃情報が3件以上あったよ: 緯度:{}, 経度:{}"
                .format(str(latitude), str(longitude))
            )
    

def BroadcastMsg(msg):
    line_bot_api.broadcast(TextSendMessage(text=msg,
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(
                                        action=LocationAction(label="ここを押して報告するこん！")
                                    )                                   
                                ])))  

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    recieve_message = event.message.text
    reply_message = None

    if recieve_message in ["ぐー", "ちょき", "ぱー"]:
        reply_message = handle_janken(event)
        return
    elif recieve_message == "reset db" :
        handle_sql.drop()
        handle_sql.init()
        reply_message = TextSendMessage(text="reset")
    elif recieve_message == "show db" :
        reply_message = TextSendMessage(text=str(handle_sql.get()))
    elif recieve_message == "broadcast":
        BroadcastMsg('ぼく')
    elif len(recieve_message.splitlines())>2 and recieve_message.splitlines()[0]=="notify":
        lines = recieve_message.splitlines()
        lines.pop(0)
        notify = "\n".join(lines)
        BroadcastMsg(notify)
    elif recieve_message == "init":
        reply_message = TextSendMessage(
                                     text="私を発見したらボタンで報告するんだこん！",
                                     quick_reply=QuickReply(items=[
                                         QuickReplyButton(
                                             action=LocationAction(label="ここを押して報告するこん！")
                                         )
                                     ]))
    else:
        reply_message = TextSendMessage(text="Unknown message type")

    if reply_message:
        line_bot_api.reply_message(event.reply_token, reply_message)


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    line_bot_api.push_message(user_id, TextSendMessage(text="登録感謝だこん！🦊🦊🦊"))
    line_bot_api.push_message(user_id, TextSendMessage(
                                     text="私を発見したらボタンで報告するんだこん！",
                                     quick_reply=QuickReply(items=[
                                         QuickReplyButton(
                                             action=LocationAction(label="ここを押して報告するこん！")
                                         )
                                     ])))
                                     
                                     
if __name__ == "__main__":
    app.run()
