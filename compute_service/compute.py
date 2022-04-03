import numpy as np
from numpy.matlib import repmat
import scipy.integrate as si
import control.matlab as cm
cm.use_numpy_matrix(False) # 让 control 库使用 array 存储矩阵

from jacobian import jacobian
from miqp import MIQP
import path
import ode

# 笛卡尔坐标转极坐标，支持传入数组
def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)

# 根据船舶当前位置搜索最近的一段参考航迹，作为优化计算中的参数
def update_path(ship):
    p_begin = ship.x0[0 : 1]
    lines = p_begin - ship.ref_state[:, 0 : 1]
    ds = np.sqrt(np.sum(lines ** 2, axis = 1))
    (index, ) = np.where(ds <= np.min(ds))
    pre_ref = ship.ref_state[index[-1] + 1 : index[-1] + ship.steps + 1, :]
    if pre_ref.shape[0] < ship.steps:
        pre_ref = ship.ref_state[-ship.steps:, :]
    
    check_heading = ship.x0[2]
    ref_heading = pre_ref[:, 2]
    for i in range(ship.steps):
        while ref_heading[i] - check_heading > np.pi:
            ref_heading[i] = ref_heading[i] - 2 * np.pi
        while ref_heading[i] - check_heading < -np.pi:
            ref_heading[i] = ref_heading[i] + 2 * np.pi
        # check_heading = ref_heading   # 此行在原matlab程序中出现，但是有逻辑问题
    pre_ref[:, 2] = ref_heading
    ship.wt = np.reshape(pre_ref, ship.num_u * ship.steps)

# 优化计算与路径跟随
def path_follow(ship):
    # 约束条件 Ax <= b
    A_u = np.block([[ship.select.ut], [-ship.select.ut]])
    av = np.dot(ship.select.vt, ship.Bt)
    A_v = np.block([[av], [-av]])

    if ship.wsfc == 0:
        A = np.block([[A_u], [A_v]])
    else:
        tm = np.dot(ship.select.surge, ship.select.ut)
        A_surge = np.block([[tm - ship.select.tau_ut], [tm + ship.select.tau_ut]])
        A_engine = np.block([[ship.select.st], [-ship.select.st]])
        A = np.block([[A_u], [A_v], [A_engine]])

    b_u = repmat(ship.max_u, 1, 2 * ship.steps)[0, :]
    tm = np.dot(ship.select.vt, ship.x_et + np.dot(ship.At,
        (ship.x0 - ship.x0)) - np.dot(ship.Bt, ship.u0))
    b_v =  np.block([repmat(ship.max_v, 1, ship.steps) - tm,
        -repmat(ship.min_v, 1, ship.steps) + tm])[0, :]

    if ship.wsfc == 0:
        b = np.block([b_u, b_v])
    else:
        b_surge = np.zeros(2 * ship.steps)
        tm = np.zeros(ship.steps)
        b_engine = np.block([repmat(ship.eff_tau_max, 1, ship.steps) - tm,
            -repmat(ship.eff_tau_max, 1, ship.steps) - tm])[0, :]
        b = np.block([b_u, b_v, b_engine])
    # print(A, b)

    # 目标函数 0.5x'Hx + fx
    C1t = np.dot(np.dot(ship.Alpha, ship.Ct), ship.At)
    D12t = -ship.Alpha
    D13t = np.dot(np.dot(ship.Alpha, ship.Ct), ship.Bt)
    E1t = np.dot(ship.Alpha, np.dot(ship.Ct, ship.x_et) -
            np.dot(np.dot(ship.Ct, ship.At), ship.x0) -
            np.dot(np.dot(ship.Ct, ship.Bt), ship.u0))
    D33t = ship.wsfc * (ship.select.tau_ut - ship.select.st)
    Cvct = np.dot(ship.Wvc, np.dot(ship.Ct, ship.At))
    D2vct = -np.dot(ship.Wvc, np.eye(ship.num_u * ship.steps))
    D3vct = np.dot(ship.Wvc, np.dot(ship.Ct, ship.Bt))
    Evct = np.dot(ship.Wvc, np.dot(ship.Ct, ship.x_et) -
            np.dot(ship.Ct, np.dot(ship.At, ship.x0)) -
            np.dot(ship.Ct, np.dot(ship.Bt, ship.u0)))
    D53t = np.dot(ship.gamma, ship.select.ut)
    c = [1, 0, 1, 0, 3]
    f = c[0] * np.dot((np.dot(C1t, ship.x0) + np.dot(D12t, ship.wt) + E1t).T,
            D13t) + c[1] * 0 + c[2] * 0 + c[3] * np.dot((np.dot(Cvct, ship.x0) +
            np.dot(D2vct, ship.wt) + Evct).T, D3vct)
    H = c[0] * np.dot(D13t.T, D13t) + c[1] * 0 + c[2] * np.dot(D33t.T,
            D33t) + c[3] * 0 + c[4] * np.dot(D53t.T, D53t)
    # print(H, f)

    # 求解MIQP
    opt_val, ut = MIQP(H, f, A, b, ship.lbt, ship.ubt, ship.u0)
    # print(opt_val)

    # 更新预测轨迹
    ship.u0 = ut

# 一步更新计算
def update(ship):
    ut = np.dot(ship.select.ut, ship.u0)
    xt = np.array([])
    x0 = ship.x0.copy()
    for i in range(ship.steps):
        tau = ut[i * ship.num_u : (i + 1) * ship.num_u]
        r = si.solve_ivp(ode.dx, t_span = (0, 1), y0 = x0, args = (ship, tau))
        x0 = r.y[:, -1].T
        xt = np.append(xt, x0)
    ship.x_et = xt

    A = np.eye(ship.num_state)
    ship.At = np.array([])
    B = np.array([])
    B0 = np.array([])

    ship.x_e = ship.x0
    for st in range(1, ship.steps + 1):
        # 计算雅各比矩阵
        A_jcb = jacobian(ship)

        # 连续状态空间转离散状态空间
        model_c = cm.ss(A_jcb, ship.B, ship.C, 0)
        model_d = cm.c2d(model_c, ship.ts)
        if ship.At.shape[0] == 0:
            ship.At = np.dot(A, model_d.A)
        else:
            ship.At = np.block([[ship.At], [np.dot(A, model_d.A)]])
        A = model_d.A

        if st == 1:
            ship.Bt = model_d.B
            B = model_d.B
        else:
            M = np.dot(model_d.A, B)
            ship.Bt = np.block([[ship.Bt, np.zeros((ship.Bt.shape[0], model_d.B.shape[1]))], [M, model_d.B]])
            B = np.block([M, model_d.B])    

        model_c = cm.ss(A_jcb, ship.B0, ship.C, 0)
        model_d = cm.c2d(model_c, ship.ts)
        if st == 1:
            ship.B0t = model_d.B
            B0 = model_d.B
        else:
            M = np.dot(A_jcb, B0)
            ship.B0t = np.block([[ship.B0t, np.zeros((ship.B0t.shape[0], model_d.B.shape[1]))], [M, model_d.B]])
            B0 = np.block([M, model_d.B])
        ship.x_e = ship.x_et[(st - 1) * ship.num_state : st * ship.num_state]
    
    # 更新当前预测时间内的参考轨迹
    update_path(ship)

    # 求解优化问题
    path_follow(ship)

    # 求解ODE计算十步预测轨迹
    ut = np.dot(ship.select.ut, ship.u0)
    xt = np.array([])
    x0 = ship.x0.copy()
    for i in range(ship.steps):
        tau = ut[i * ship.num_u : (i + 1) * ship.num_u]
        r = si.solve_ivp(ode.dx, t_span = (0, 1), y0 = x0, args = (ship, tau))
        x0 = r.y[:, -1].T
        xt = np.append(xt, x0)
    ship.x_et = xt
    ship.u0 = np.block([ship.u0[ship.num_input:], ship.u0[-ship.num_input:]])
