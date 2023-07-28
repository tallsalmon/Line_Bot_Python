import json

user_status={}

class MessageHandler:
    def reply(receivedEvent):
        #print(receivedEvent)
        text=receivedEvent.message.text
        #text=str(receivedEvent.source['userId'])

        #userIdとtypeを無理くり取得
        source=str(receivedEvent.source)
        r=source.rfind('"')
        l=source.rfind('"',0,r-1)
        id=source[l+1:r]
        l=source.find('"')
        l=source.find('"',l+1)
        l=source.find('"',l+1)
        r=source.find('"',l+1)
        type=source[l+1:r]
        #text=id
        
        #id=receivedEvent.source[userId]
        if type=='user':
            if id not in user_status:
                user_status[id]=0

            if user_status[id]==0:
                text='こんにちは。本日はイタチ判別にご協力いただき誠にありがとうございます。これからいくつか質問をさせていただきますので、できるだけ正確にお答えしていただけるようよろしくお願いいたします。'
                user_status[id]+=1

        text=type
        #answer=text
        #text='A'
        return text
