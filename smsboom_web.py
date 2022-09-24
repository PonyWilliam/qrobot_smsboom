import json
import string
from time import sleep
from flask import Flask,request
from smsboom import runboom
from threading import Thread
app = Flask(__name__)

temp = 0

@app.route('/')
def hello():
    return "hello world"

@app.route('/phone/<phone>')
def phone(phone:string):
    key = request.args.get("key")
    if key != "qrobot_dadi":
        return json.dumps({
            "status":100,
            "msg":"你无权使用本接口"
        })
    global temp
    if temp == 1:
        # 这个暂时没啥用，用限时间吧。
        return json.dumps({
            "status":101,
            "msg":"轰炸线程正忙，请稍后再试"
        })
    if len(phone) != 11:
        return json.dumps({
            "status":102,
            "msg":"请输入正确的手机号"
        })
    # 调用轰炸函数
    temp = 1
    Thread(target=runboom,args=(phone,False)).start() # 创建一个线程去执行
    return json.dumps({
        "status":200,
        "msg":"开始轰炸" + phone
    })

def count():
    while True:
        global temp
        temp = 0
        sleep(60) # 60s内只允许一个轰炸

if __name__ == "__main__":
    Thread(target=count).start()
    app.run(port=80,host="0.0.0.0")