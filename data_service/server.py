import json
import uuid
from flask import Flask, request, jsonify
app = Flask(__name__)
from flask_cors import CORS
CORS(app, supports_credentials=True) # 允许跨域请求
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # 设置Flask的Log输出级别，减少回显信息

import serial
import time

# 读取DAQM4206所有通道数据，此函数可作为参考
def read_DAQM4206(port,baudrate):
    s = serial.Serial(port = port, baudrate = baudrate, parity='N') #打开端口
    code = "01 04 00 00 00 08 F1 CC" #读数据的命令码
    n = s.write(bytes.fromhex(code))

    time.sleep(0.1)
    num = s.inWaiting()

    data = []
    if num:
        batch = s.read(num)
        for i in range(8):
            raw = int.from_bytes(batch[3+2*i:5+2*i],byteorder='little') #读取一个通道的数据
            data.append(raw)
    serial.Serial.close(s)
    return data # 返回的数据尚未量化，因为有的通道是电流信号，有的是电压信号，量化参照不同

# 从采集卡读取数据，处理后返回传感器真实量测值，【这个函数需要你接上传感器，并按相关格式转换后实现和验证】
def get_data_from_DAQM():
    
    return {'angle':30,'force':15}

# 从AIS设备读取信息，返回船舶位置，【这个函数需要你从AIS设备读取数据并解析出定位信息】
def get_data_from_AIS():

    return {'loc':[0,0]} #纬度在前，经度在后

# 响应数据请求
@app.route('/data', methods=['GET'])
def data_handler():
    #id = request.args.get('id')
    DAQM = get_data_from_DAQM()
    AIS = get_data_from_AIS()
    return jsonify(loc=AIS['loc'],angle=DAQM['angle'],force=DAQM['force'])

# 启动Web服务
app.run(debug = False, host='0.0.0.0', port=9876 ,threaded=False)
