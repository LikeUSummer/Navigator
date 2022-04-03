import numpy as np
#import matplotlib.pyplot as plt

import path
import compute
from ship import Ship

#船舶实例化
ship = Ship()

#规划航迹
ship.rough_path = np.block([[0, 0],[40, 0],[90, 40]])

#初始化船舶状态
ship.x0 = np.block([0, 0, 0, 0.8, 0, 0])

#迭代计算
for i in range(50):
    compute.update(ship)
    print(i,ship.x_et[0 : 6])
    ship.x0 = ship.x_et[0 : 6]
