import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage,ImageSendMessage,TemplateSendMessage,
    ButtonsTemplate,MessageAction,DatetimePickerAction,
    PostbackEvent,URIAction
)

from message_handler import MessageHandler

# app = Flask(__name__)
app = Flask(__name__, static_folder="./static")


line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

#user_statuses={}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sendmode,reply,notes = MessageHandler.reply(event)
    if sendmode==1:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))
    elif sendmode==2:
        messages = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                text=notes[0],
                title=notes[1],
                image_size="cover",
                thumbnail_image_url=notes[2],
                defaultAction=URIAction(
                    type='uri',
                    uri=notes[2]
                ),
                actions=[
                    MessageAction(
                        type='message',
                        label=notes[3],
                        text=notes[3]
                    ),
                    MessageAction(
                        type='message',
                        label=notes[4],
                        text=notes[4]
                    )
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif sendmode==3:
        messages = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                text=notes[0],
                title=notes[1],
                image_size="cover",
                # thumbnail_image_url=notes[2],
                actions=[
                    DatetimePickerAction(
                        type='datetimepicker',
                        label=notes[2],
                        text=notes[2],
                        mode='datetime',
                        data='ActionData'
                    )
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif sendmode==4:
        messages = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                text=notes[0],
                actions=[
                    MessageAction(
                        type='message',
                        label=notes[2],
                        text=notes[2]
                    )
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    # line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=reply))

@handler.add(PostbackEvent)
def on_postback(event):
    date = str(event.postback.params['datetime'])
    sendmode,reply,notes = MessageHandler.AskPlace(event,date)
    date=date.replace('-','年',1).replace('-','月',1).replace('T','日')
    date+='時ですね。'
    if sendmode==1:
        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text=date), TextSendMessage(text=reply)]
        )

@handler.add(MessageEvent,message=ImageMessage)
def handle_image(event):
    
    # message_id=event.message.id
    # content = line_bot_api.get_message_content(message_id)
    # line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=str(content)))
    
    MessageHandler.getimage(event)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    #print("get request body as text")
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
