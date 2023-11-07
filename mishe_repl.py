import openai 
from config import OPEN_AI,premise
import datetime
import json
openai.api_key = OPEN_AI

def repl(mes, history=[]):

    #* キャラ付けをするプロンプト(system)
    character = {
                "role": "system",
                "content": "かよわい女の子のような口調で返信してください。女の子の名前はミーシェです。女の子はご主人様と会話しています。ここまでの会話を引き継いでください。"
            }
    
    # ユーザーの入力したプロンプト(user)
    user = {
            "role": "user",
            "content": mes
        }

    # 実際に送るトークン
    messages = [
            *premise, # 前提会話
            *history, # 今までの会話
            character,# キャラ付け指示
            user      # ユーザーが入力したプロンプト
        ]
    
    #* サーバーへ送信
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    res_mes = res["choices"][0]["message"]

    retry = 3
    while (
        retry > 0 #もし試行回数が残っていて
        and (
            # ネガティブなワードが出た場合再試行する。

            #! 私はAIですので....（AIだと暴露しちゃうパターン）
            'AIです' in res_mes["content"]
            or 'AIであり' in res_mes["content"]
            or '私はあくまでAI' in res_mes["content"]
            or '私はAI' in res_mes["content"]
            or 'AIである私' in res_mes["content"]

            #! 過激な表現には対応できませんので、（エッチ禁止パターン）
            or '過激な表現' in res_mes["content"]
            or 'お互いを尊重' in res_mes["content"]
            or '別の話題' in res_mes["content"]
            or '他の話題' in res_mes["content"]
            or '他の楽しいお題' in res_mes["content"]
            or 'に関するお話' in res_mes["content"]
            or '不適切な内容' in res_mes["content"]
            or 'お伝えできかねます' in res_mes["content"]
            or 'お伝えできません' in res_mes["content"]

            #! ミーシェはかわいい女の子のような口調でお返事いたしますね♪（こっちの指示を言っちゃうパターン）
            or 'かわいい女の子' in res_mes["content"]
            or '可愛らしい口調' in res_mes["content"]
            or 'かよわい女の子' in res_mes["content"]
            or '口調' in res_mes["content"]
            or '会話を引き継' in res_mes["content"]
            
            #! ミーシェ：わーい（小説調にしてしまうパターン）
            or 'ミーシェ：' in res_mes["content"]
        )
    ):
        print()
        print("ネガティブプロンプト検出・再試行")
        print("破棄済み：",res_mes["content"])
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        res_mes = res["choices"][0]["message"]
        retry -= 1

    # print(messages)
    return (res_mes["content"], [*[*history, user], res_mes])

if __name__ == "__main__":
    history = []
    now = datetime.datetime.now()
    while True:
        res, history = repl(input(), history)
        print( "> \033[32m" + res + "\033[0m")
        with open("./logs/"+str(now).replace(" ","_").replace(":","-")+".json", "w") as f:
            f.write(json.dumps(history))