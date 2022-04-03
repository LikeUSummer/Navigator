import numpy as np
import scipy.integrate as si
import matplotlib.pyplot as plt

def dx(t, x, ship, tau):
    m11 = ship.M[0, 0]
    m22 = ship.M[1, 1]
    m23 = ship.M[1, 2]
    m32 = ship.M[2, 1]
    m33 = ship.M[2, 2]

    d11 = ship.D[0, 0]
    d22 = ship.D[1, 1]
    d23 = ship.D[1, 2]
    d32 = ship.D[2, 1]
    d33 = ship.D[2, 2]

    tao_u = tau[0]
    tao_v = tau[1]
    tao_r = tau[2]

    r11 = np.cos(x[2])
    r12 = np.sin(x[2])

    return [
        r11 * x[3] - x[4] * r12, 
        r11 * x[4] + x[3] * r12, 
        x[5], 
        (tao_u - d11 * x[3] - ship.Yr * x[5] * (x[5]) - ship.Yv * x[4] * (x[5]) +
            ship.m * x[4] * (x[5]) + ship.m * x[5] * ship.xg * (x[5])) / m11, 
        -(m23 * tao_r - m33 * tao_v + d23 * m33 * x[5] - d33 * m23 * x[5] +
            d22 * m33 * x[4] - d32 * m23 * x[4] - ship.Xu * m33 * x[3] * x[5] +
            ship.Yr * m23 * x[5] * x[3] - ship.Xu * m23 * x[3] * x[4] +
            ship.Yv * m23 * x[4] * x[3] + ship.m * m33 * x[3] * x[5] +
            ship.m * m23 * x[3] * x[4] - ship.m * m23 * x[4] * x[3] -
            ship.m * m23 * x[5] * ship.xg * x[3]) / (m22 * m33 - m23 * m32), 
        (m22 * tao_r - m32 * tao_v + d23 * m32 * x[5] - d33 * m22 * x[5] +
            d22 * m32 * x[4] - d32 * m22 * x[4] - ship.Xu * m32 * x[3] * x[5] +
            ship.Yr * m22 * x[5] * x[3] - ship.Xu * m22 * x[3] * x[4] +
            ship.Yv * m22 * x[4] * x[3] + ship.m * m32 * x[3] * x[5] +
            ship.m * m22 * x[3] * x[4] - ship.m * m22 * x[4] * x[3] -
            ship.m * m22 * x[5] * ship.xg * x[3]) / (m22 * m33 - m23 * m32)
    ]

#按状态空间方程定义的更精简形式，但是和上面的求解结果有一点差异
def dx1(t, x, ship, tau):
    Z3 = np.zeros((3, 3))
    s = np.sin(x[2])
    c = np.cos(x[2])
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    C = np.array(
    [[0, 0, ship.Yv * x[4] + ship.Yr * x[5] - ship.m * x[4]], 
    [0, 0, -ship.Xu * x[3] + ship.m * x[3]], 
    [ship.m * x[4] - ship.Yv * x[4] - ship.Yr * x[5], ship.Xu * x[3] - ship.m * x[3], 0]])
    A = np.block([[Z3, R], [Z3, np.dot(-ship.MI, (C + ship.D))]])
    return np.dot(A, x) + np.dot(ship.B0, tau)

#测试求解船舶运动方程
# t = np.arange(0, 20, 0.001)
# r = si.solve_ivp(dx, t_span = [0, 1], y0 = [0, 1, 0.5, 1, -1, 2], args = (ship, [1, 1, 1]))
# print(r.t)
# plt.plot(r.y[0, :], r.y[1, :])
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()
# print(dx(1, [0, 1, 0.5, 1, -1, 2], ship, [1, 1, 1]))
