#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author:qiu_lzsnmb
@file:run.py
@time:2022/06/29
"""
import datetime
import time

from xcb import XCB
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, Namespace

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    cotest = {}
    return render_template('index.html', **cotest)


class MyCustomNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.xcb = None

    def on_connect(self):
        emit('connection', {'data': 'Connected'})

    def on_disconnect(self):
        print('Client disconnected')

    def on_xcb_conn(self, data):
        self.xcb = XCB(f"{data['ip']}:{data['port']}", "网页", data['courseid'])
        r = self.xcb.getCompanyCode()
        emit('xcb_con', {'code': '200', 'msg': '连接成功！', 'data': r})

    def on_getCompanyCode(self):
        emit('getCompanyCode', {'code': '200', 'msg': '公司代码获取成功！'})

    def on_getHistoricalDecisions(self, data):
        h = self.xcb.getHistoricalDecisions(data['time'], data['companyid'])
        if h.status_code == 200:
            with open('static/mb.html', encoding='utf-8', mode='w') as f:
                f.write(h.text)
            emit('getHistoricalDecisions', {'code': '200', 'msg': '历史决策获取成功！'})
        else:
            emit('getHistoricalDecisions', {'code': '500', 'msg': '历史决策获取失败'})

    def on_getProductDesign(self, data):
        r = self.xcb.getProductDesign(data['companyid'])
        emit('getProductDesign', {'code': '200', 'msg': r})

    def on_getCashFlow(self, data):
        r = self.xcb.getCashFlow(data['companyid'])
        emit('getCashFlow', {'code': '200', 'msg': r})


socketio.on_namespace(MyCustomNamespace())
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)
