print("计算服务初始化...")
import sys
sys.path.append('./')

from flask import Flask, request, jsonify
app = Flask(__name__)
from flask_cors import CORS
CORS(app, supports_credentials = True) # 允许跨域请求

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # 设置 Flask 的 Log 打印级别，减少回显信息

import json
import uuid
import numpy as np
import scipy.integrate as si

from ship import Ship
import compute

cache = {} # 全局计算实例缓存

def add():
    ship = Ship() # 新建船舶实例
    id = str(uuid.uuid1())
    cache[id] = ship
    return id

# 新建一个计算实例
@app.route('/add', methods = ['POST'])
def add_handler():
    data = json.loads(request.get_data(as_text = True))
    id = add()
    return jsonify(id=id, status = 0)

# 删除一个计算实例
@app.route('/delete', methods = ['GET'])
def delete_handler():
    id = request.args.get('id')
    if id in cache:
        del cache[id]
    return "delete " + id

# 修改计算实例的参数
@app.route('/modify', methods = ['POST'])
def modify_handler():
    data = json.loads(request.get_data(as_text = True))
    id = data['id']
    del data['id']
    if not id in cache:
        return jsonify(status = 1)

    for k in data.keys():
        if isinstance(data[k], list):
            setattr(cache[id], k, np.array(data[k]))
        else:
            setattr(cache[id], k, data[k])
    return jsonify(status = 0)

# 对指定的计算实例完成一次优化计算
@app.route('/update', methods = ['POST'])
def update_handler():
    data = json.loads(request.get_data(as_text = True))
    id = data['id']
    if not id in cache:
        return jsonify(status = 1)

    cache[id].x0 = np.array(data['state'])
    compute.update(cache[id])

    state = cache[id].x_et[0 : 6].tolist() # 预期状态
    speed = np.linalg.norm(cache[id].x_et[3 : 5])
    points = []
    for i in range(cache[id].steps):
        points.append(cache[id].x_et[i * 6 : i * 6 + 2].tolist())
    return jsonify(status = 0, state = state, speed = speed, points = points)


# 进行一次预计算，以初始化计算库
id = add()
cache[id].rough_path = np.array([[0, 0], [40, 0], [90, 40]])
cache[id].x0 = np.array([0, 0, 0, 0.8, 0, 0])
compute.update(cache[id])
print("初始化完成，服务运行中...")
# 启动 Web 服务
app.run(debug = False, host = '0.0.0.0', port = 6789,
    threaded = False) # 由于求解器要运行在主线程，所以Flask只能以单线程模式运行
