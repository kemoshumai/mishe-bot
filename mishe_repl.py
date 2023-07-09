import openai 
from config import OPEN_AI
import datetime
import json
openai.api_key = OPEN_AI

def repl(mes, history=[]):
    character = {
                "role": "system",
                "content": "かよわい女の子のような口調で返信してください。女の子の名前はミーシェです。女の子はご主人様と会話しています。"
            }
    user = {
            "role": "user",
            "content": mes
        }
    message = []
    if len(history) != 0:
        message = history
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[*message, character, user]
    )
    message.append(user)
    res_mes = res["choices"][0]["message"]
    history = message
    return (res_mes["content"], [*history, res_mes])

if __name__ == "__main__":
    history = []
    now = datetime.datetime.now()
    while True:
        res, history = repl(input(), history)
        print( "> \033[32m" + res + "\033[0m")
        with open("./logs/"+str(now).replace(" ","_").replace(":","-")+".json", "w") as f:
            f.write(json.dumps(history))