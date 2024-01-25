import json

import datetime

import os
import dropbox
from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))

# Dropbox(Salmonfs)のアクセストークン
DROPBOX_ACCESS_TOKEN = 'sl.BnHRHWk2rXzCQdmN0qckxTISBxln8jxuAQw-2gllG4gjeLbgUU1D1gIavCoy0C9qXeLmm4XMKSnI3_jV1OIqJwew8c2N4fQiFwd9YASQEnDLforzgksimjxKSH0Kt9eJt6Doh6i54Ifp'
# Dropbox(Salmonfs)のリフレッシュトークン
DROPBOX_REFRESH_TOKEN=os.getenv('CHANNEL_REFRESH_TOKEN')
# Dropboxのフォルダ
# Dropboxのルートにこの名前のフォルダを事前に作っておく必要がある
DROPBOX_ROOT = '/fujishima_weasel/'
DROPBOX_IMAGE_ROOT='/fujishima_image/'
client = dropbox.Dropbox(app_key='ng3r13wmw0k35g9',app_secret='abnb48hn78crx6p',oauth2_refresh_token='2fl8VXXfWdsAAAAAAAAAATAUF3oa2VqnRLvWV5E0HFsEgZhnYDIg-UYMjcPh6oIq')

send_num=[0]

user_status={}
user_answer={}#{userid:[date,place,name,talerate(尾率 はいorいいえ),whitepoint(白斑 はいorいいえ),colordif(毛色の違い はいorいいえ),result,id,dropbox画像ファイルパス]}
itachi_point={}#二ホンイタチの特徴に当てはまる場合+1,シベリアイタチの特徴に当てはまる場合+0　合計が2以上で二ホンイタチ
user_image={}#写真を上げてくれた枚数（イタチの画像の名前に使用）
send_mode={}#ユーザーに送るメッセージの種類を決定（1のときテキストメッセージ、2のときテンプレートメッセージ）

class MessageHandler:

    def makenotes(status):
        if status==6:
            notes=[
                '尾率は尾長（尻尾の長さ）を頭胴長（頭から尻尾の付け根までの長さ）で割ると求めることができます。',
                '尾率が５０％以上かどうか教えて下さい。',
                'https://raw.githubusercontent.com/tallsalmon/Line_Bot_Python/main/static/birituwithsamplewith.jpg',
                'はい(50%以上)',
                'いいえ(50%未満)'
            ]
        elif status==7:
            notes=[
                '写真を例にお答えください。',
                '鼻上中央に白斑はありますか。',
                'https://github.com/tallsalmon/Line_Bot_Python/blob/main/static/%E9%BC%BB%E4%B8%AD%E5%A4%AE%E5%88%A4%E5%88%A5%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB.jpg?raw=true',
                'はい(白斑あり)',
                'いいえ(白斑なし)'
            ]
        elif status==8:
            notes=[
                '写真を例にお答えください。 (無ければシベリアイタチ/有ればニホンイタチ)',
                '最後に頬と後ろ足の毛色に差はありますか。',
                'https://github.com/tallsalmon/Line_Bot_Python/blob/main/static/%E8%89%B2%E5%B7%AE%E3%81%82%E3%82%8A%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB.jpg?raw=true',
                'はい(色差あり)',
                'いいえ(色差なし)'
            ]
        elif status==2:
            notes=[
                '　',
                '捕獲した日時はいつですか？',
                '日時を入力'
            ]
        return notes

    def AskPlace(receivedEvent,Date):
        source=str(receivedEvent.source)
        r=source.rfind('"')
        l=source.rfind('"',0,r-1)
        id=source[l+1:r]
        l=source.find('"')
        l=source.find('"',l+1)
        l=source.find('"',l+1)
        r=source.find('"',l+1)
        type=source[l+1:r]
        notes=[]
        text=str(id)
        if type=='user':
            if user_status[id]==3:
                text='捕獲した場所を教えて下さい。以下のようにお答えください。例：福井県〇〇市〇〇町〇〇番地'
                user_status[id]=4
                user_answer[id].append(str(Date))#日時の記録
                send_mode[id]=1
        return send_mode[id],text,notes
        # return 1,text,notes
    
    
    def reply(receivedEvent):
        
        # #print(receivedEvent)
        text=receivedEvent.message.text
        # # text=str(receivedEvent.source)

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
        text=id
        # text=str(receivedEvent.source)

 
        notes=[]
        # m = re.search(r'userId":.+', text)
        # t = m.group()
        # userid = t[10:-2]

        # f = open('myfile.txt', 'w')
        # f.write(text)
        # f.close()
        # # アップロードしたいファイル
        # local_filepath = 'myfile.txt'
        # send_num[0]+=1
        # アップロード先のファイル名（アップロードしたいファイルと同じ名前でもよい）
        # dropbox_filepath = 'test'+str(send_num[0])+'.txt'
        # ファイルアップロード
        # client.files_upload(open(local_filepath, "rb").read(), os.path.join(DROPBOX_ROOT, dropbox_filepath))


        
        #print('B')
        # id=receivedEvent.source[userId]
        if type=='user':
            if id not in user_status:
                user_status[id]=0
                send_mode[id]=1

            if user_status[id]==0:
                notes=['こんにちは。本日はイタチ判別にご協力いただき誠にありがとうございます。これからいくつか質問をさせていただきますので、できるだけ正確にお答えしていただけるようよろしくお願いいたします。まずは捕獲した記録を残したいので、以下の３つの質問に答えてください。',
                      '',
                      '開始']
                user_status[id]=1
                user_answer[id]=[]
                itachi_point[id]=0
                user_status[id]=2
                send_mode[id]=4

            elif user_status[id]==2:
                text='捕獲した日時はいつですか?'
                user_status[id]=3
                send_mode[id]=3
                notes=MessageHandler.makenotes(2)

            elif user_status[id]==3:
                text='捕獲した場所を教えて下さい。以下のようにお答えください。例：福井県〇〇市〇〇町〇〇番地'
                user_status[id]=4
                user_answer[id].append(receivedEvent.message.text)#日時の記録
                send_mode[id]=1

            elif user_status[id]==4:
                text='捕獲者のお名前を教えて下さい。'
                user_status[id]=5
                user_answer[id].append(receivedEvent.message.text)#場所
                send_mode[id]=1

            elif user_status[id]==5:
                text='次に捕獲したイタチの状態について以下の３つの質問に答えてください。'
                notes=['次に捕獲したイタチの状態について以下の３つの質問に答えてください。',
                      '',
                      '質問を表示']
                user_status[id]=6
                user_answer[id].append(receivedEvent.message.text)#名前
                send_mode[id]=4
                

            elif user_status[id]==6:
                text='まず、尾率が５０％以上かどうか教えて下さい。尾率は尾長（尻尾の長さ）を頭胴長（頭から尻尾の付け根までの長さ）で割ると求めることができます。'
                user_status[id]=7
                send_mode[id]=2
                notes=MessageHandler.makenotes(6)

            elif receivedEvent.message.text=='はい(50%以上)' or receivedEvent.message.text=='いいえ(50%未満)':
                text='鼻上中央に白斑はありますか。写真を例にお答えください。'
                user_status[id]=8
                send_mode[id]=2
                notes=MessageHandler.makenotes(7)
                user_answer[id].append(receivedEvent.message.text)#尾率
                if user_answer[id][-1]=='いいえ(50%未満)':
                    itachi_point[id]+=1
                elif user_answer[id][-1]=='はい(50%以上)':
                    itachi_point[id]+=0
                else:
                    itachi_point[id]=100

            elif receivedEvent.message.text=='はい(白斑あり)' or receivedEvent.message.text=='いいえ(白斑なし)':
                text='最後に頬と後ろ足の毛色に差はありますか。写真を例にお答えください。 (無ければシベリアイタチ/有ればニホンイタチ)'
                user_status[id]=9
                send_mode[id]=2
                notes=MessageHandler.makenotes(8)
                user_answer[id].append(receivedEvent.message.text)#白斑
                if user_answer[id][-1]=='いいえ(白斑なし)':
                    itachi_point[id]+=1
                elif user_answer[id][-1]=='はい(白斑あり)':
                    itachi_point[id]+=0
                else:
                    itachi_point[id]=100

            elif receivedEvent.message.text=='はい(色差あり)' or receivedEvent.message.text=='いいえ(色差なし)':
                send_mode[id]=1
                user_answer[id].append(receivedEvent.message.text)#毛色の差
                if user_answer[id][-1]=='はい(色差あり)':
                    itachi_point[id]+=1
                elif user_answer[id][-1]=='いいえ(色差なし)':
                    itachi_point[id]+=0
                else:
                    itachi_point[id]=100

                if itachi_point[id]>=100:
                    result='不明'
                elif itachi_point[id]>=2:
                    result='二ホンイタチ'
                else:
                    result='シベリアイタチ'
                user_answer[id].append(result)
                user_answer[id].append(str(id))
                text='ありがとうございます。判定結果は「'+result+'」でした。今後、この判別方式が有効かどうかを検証するために、今回捕獲されたイタチの写真提供にご協力いただけないでしょうか。全身の写真、顔のアップの写真を提供いただけるとありがたいです。（写真は何枚でも送信できます）写真の送信が完了しましたら「完了」と送信してください。'
                user_status[id]=10
                
                dt_now = str(datetime.datetime.now())
                # client.files_create_folder('fujishima_image/'+dt_now+str(user_answer[id][2]))
                # user_answer[id].append('fujishima_image/'+dt_now+str(user_answer[id][2]))
                
            elif user_status[id]==10:
                text='これで質問は終わりです。イタチ判別にご協力いただきありがとうございました。ほかの個体を送信する場合はもう一度「イタチ」と送信してください。'
                user_status[id]=0
                send_mode[id]=1
                # text+=str(user_status[id])
                f = open(id+'.txt', 'w')
                f.write(str(user_answer[id]))
                f.close()
                # アップロードしたいファイル
                local_filepath = id+'.txt'
                # send_num[0]+=1
                #アップロード先のファイル名（アップロードしたいファイルと同じ名前でもよい）
                tmpdate=''
                for i in user_answer[id][0]:
                    if i!='/':
                        tmpdate+=i
                dropbox_filepath = 'test'+str(user_answer[id][2])+tmpdate+'.txt'
                #ファイルアップロード
                client.files_upload(open(local_filepath, "rb").read(), os.path.join(DROPBOX_ROOT, dropbox_filepath))
        # answer=text
        #text='A'
        return send_mode[id],text,notes

    
    def getimage(receivedEvent):
        #userIdとtypeを無理くり取得
        source=str(receivedEvent.source)
        r=source.rfind('"')
        l=source.rfind('"',0,r-1)
        id=source[l+1:r]

        if len(user_answer[id])<9:
            return
        
        if id not in user_image:
            user_image[id]=0
        user_image[id]+=1
        filename=user_answer[id][2]+str(user_image[id])

        message_id=receivedEvent.message.id
        content = line_bot_api.get_message_content(message_id)
        with open(filename+".txt", "wb") as f:
            for c in content.iter_content():
                f.write(c)
        f.close()
        #ファイルアップロード
        # client.files_save_url('/fujishima_image/'+filename+'.jpg',content)
        client.files_upload(open(filename+".txt", "rb").read(), os.path.join(DROPBOX_IMAGE_ROOT, filename+".jpg"))
        # with open(DROPBOX_IMAGE_ROOT+filename+".jpg", "wb") as f:
            # for c in content.iter_content():
                # f.write(c)
        # f.close()


               
