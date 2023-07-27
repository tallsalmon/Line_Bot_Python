import json

user_status={}

class MessageHandler:
    def reply(receivedEvent):
        text=receivedEvent.message.text
        userId=receivedEvent.source.userId
        if receivedEvent.source.type=='user':
            if userId not in user_status:
                user_status[userId]=0

            if user_status[userId]==0:
                text='こんにちは。本日はイタチ判別にご協力いただき誠にありがとうございます。これからいくつか質問をさせていただきますので、できるだけ正確にお答えしていただけるようよろしくお願いいたします。'
                user_status[userId]+=1
        #answer=text
        #text='A'
        return text
