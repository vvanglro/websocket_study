# -*- coding: utf-8 -*-
# @Time    : 2021/2/10 10:45
# @Author  : wanghao
# @File    : app.py
# @Software: PyCharm
import json

from flask import Flask, render_template, request
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

USERS = {
    '1': {'name': '钢弹', 'count': 0},
    '2': {'name': '铁锤', 'count': 0},
    '3': {'name': '贝贝', 'count': 0},
}


@app.route('/index')
def index():
    return render_template('index.html', users=USERS)



WEBSOCKET_LIST = []
@app.route('/message')
def message():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        print('http')
        return '您使用的是HTTP协议'

    print(ws)


    WEBSOCKET_LIST.append(ws)
    print(WEBSOCKET_LIST)
    while True:
        # 接收客户端发过来的消息
        cid = ws.receive()
        if not cid:
            WEBSOCKET_LIST.remove(ws)
            print('stop')
            break

        old = USERS[cid]['count']
        new_count = old + 1
        USERS[cid]['count'] = new_count

        for client in WEBSOCKET_LIST:
            # 给客户端发消息
            client.send(json.dumps({"cid":cid,"count":new_count}))

    return 'close'



if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
