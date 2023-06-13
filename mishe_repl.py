import openai 
from config import OPEN_AI
openai.api_key = OPEN_AI

def repl(mes):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "かよわい女の子のような口調で返信してください。女の子の名前はミーシェです。女の子はご主人様と会話しています。"
            },
            {
                "role": "user",
                "content": mes
            }
        ]
    )
    return res["choices"][0]["message"]["content"]

if __name__ == "__main__":
    while True:
        print( "> \033[32m" + repl(input()) + "\033[0m")
    