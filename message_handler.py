import json

user_status={}

class MessageHandler:
    def reply(receivedEvent):
        text=receivedEvent.message.text
        userId=event.source.userId
        if event.source.type=='user':
            if event.source.type not in user_status:
                user_status[userId]=0

            if user_status[userId]==0:
                text='こんにちは。本日はイタチ判別にご協力いただき誠にありがとうございます。これからいくつか質問をさせていただきますので、できるだけ正確にお答えしていただけるようよろしくお願いいたします。'

        #answer=text
        #text='A'
        return text
