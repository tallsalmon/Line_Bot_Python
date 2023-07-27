import json

user_status={}

class MessageHandler:
    def reply(receivedEvent):
        text=receivedEvent.message.text
        id=receivedEvent.source.userId
        if receivedEvent.source.type=='user':
            if id not in user_status:
                user_status[id]=0

            if user_status[id]==0:
                text='こんにちは。本日はイタチ判別にご協力いただき誠にありがとうございます。これからいくつか質問をさせていただきますので、できるだけ正確にお答えしていただけるようよろしくお願いいたします。'
                user_status[id]+=1
        #answer=text
        #text='A'
        return text
