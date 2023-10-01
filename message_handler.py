import json

import os
import dropbox

# Dropbox(Salmonfs)のアクセストークン
DROPBOX_ACCESS_TOKEN = 'sl.BnHRHWk2rXzCQdmN0qckxTISBxln8jxuAQw-2gllG4gjeLbgUU1D1gIavCoy0C9qXeLmm4XMKSnI3_jV1OIqJwew8c2N4fQiFwd9YASQEnDLforzgksimjxKSH0Kt9eJt6Doh6i54Ifp'
# Dropboxのフォルダ
# Dropboxのルートにこの名前のフォルダを事前に作っておく必要がある
DROPBOX_ROOT = '/fujishima_weasel/'
client = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

send_num=[0]

user_status={}
user_answer={}#{userid:[date,place,name,talerate(尾率 はいorいいえ),whitepoint(白斑 はいorいいえ),colordif(毛色の違い はいorいいえ)]}
itachi_point={}#二ホンイタチの特徴に当てはまる場合+1,シベリアイタチの特徴に当てはまる場合+0　合計が2以上で二ホンイタチ

class MessageHandler:
    
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
                user_answer[id]=[]
                itachi_point[id]=0

            if user_status[id]==0:
                text='こんにちは。本日はイタチ判別にご協力いただき誠にありがとうございます。これからいくつか質問をさせていただきますので、できるだけ正確にお答えしていただけるようよろしくお願いいたします。'
                user_status[id]=1

            elif user_status[id]==1:
                text='まずは捕獲した記録を残したいので、以下の３つの質問に答えてください。'
                user_status[id]=2

            elif user_status[id]==2:
                text='捕獲した日時はいつですか?'
                user_status[id]=3

            elif user_status[id]==3:
                text='捕獲した場所を教えて下さい。以下のようにお答えください。例：福井県〇〇市〇〇町〇〇番地'
                user_status[id]=4
                user_answer[id].append(receivedEvent.message.text)#日時の記録

            elif user_status[id]==4:
                text='捕獲者のお名前を教えて下さい。'
                user_status[id]=5
                user_answer[id].append(receivedEvent.message.text)#場所

            elif user_status[id]==5:
                text='次に捕獲したイタチの状態について以下の３つの質問に答えてください。'
                user_status[id]=6
                user_answer[id].append(receivedEvent.message.text)#名前

            elif user_status[id]==6:
                text='まず、尾率が５０％以上かどうか教えて下さい。尾率は尾長（尻尾の長さ）を頭胴長（頭から尻尾の付け根までの長さ）で割ると求めることができます。'
                user_status[id]=7

            elif user_status[id]==7:
                text='鼻上中央に白斑はありますか。下の写真を例にお答えください。'
                user_status[id]=8
                user_answer[id].append(receivedEvent.message.text)#尾率
                if user_answer[id][-1]=='いいえ':
                    itachi_point[id]+=1

            elif user_status[id]==8:
                text='最後に頬と後ろ足の毛色に差はありますか。下の写真を例にお答えください。 (無ければシベリアイタチ/有ればニホンイタチ)'
                user_status[id]=9
                user_answer[id].append(receivedEvent.message.text)#白斑
                if user_answer[id][-1]=='いいえ':
                    itachi_point[id]+=1

            elif user_status[id]==9:
                user_answer[id].append(receivedEvent.message.text)#毛色の差
                if user_answer[id][-1]=='はい':
                    itachi_point[id]+=1

                if itachi_point[id]>=2:
                    result='二ホン'
                else:
                    result='シベリア'
                user_answer[id].append(result+'イタチ')
                text='ありがとうございます。判定結果は「'+result+'イタチ」でした。今後、この判別方式が有効かどうかを検証するために、今回捕獲されたイタチの写真提供にご協力いただけないでしょうか。全身の写真、顔のアップの写真を提供いただけるとありがたいです。'
                user_status[id]=10
                
            elif user_status[id]==10:
                text='これで質問は終わりです。イタチ判別にご協力いただきありがとうございました。'
                user_status[id]=0
                # text+=str(user_status[id])

                f = open(id+'.txt', 'w')
                f.write(str(user_answer[id]))
                f.close()
                # アップロードしたいファイル
                local_filepath = id+'.txt'
                # send_num[0]+=1
                #アップロード先のファイル名（アップロードしたいファイルと同じ名前でもよい）
                dropbox_filepath = 'test'+str(user_answer[id][2])+str(user_answer[id][0])+'.txt'
                #ファイルアップロード
                client.files_upload(open(local_filepath, "rb").read(), os.path.join(DROPBOX_ROOT, dropbox_filepath))
        # answer=text
        #text='A'
        return text
