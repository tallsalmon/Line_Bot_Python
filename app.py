import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageMessage,ImageSendMessage
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
                text='尾率は50%以上？',
                title='質問1',
                image_size="cover",
                thumbnail_image_url="https://任意の画像URL.jpg",
                actions=[
                    MESSAGEAction(
                        type='message',
                        label='Yes',
                        text='Yes'
                    ),
                    MESSAGEAction(
                        type='message',
                        label='No',
                        text='No'
                    )
                ]
            ),
        )
        line_bot_api.reply_message(event.reply_token, messages=messages)
    # line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=reply))

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
