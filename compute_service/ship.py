import numpy as np
import numpy.matlib
import math

import path

class Struct:
    pass

class Ship:
    count = 0
    def __init__(self):
        Ship.count += 1
        # 动力学参数
        self.m = 23.8
        self.Iz = 1.76
        self.xg = 0.046
        self.Xu = -2
        self.Yv = -10
        self.Yr = 0
        self.Nv = 0
        self.Nr = -1
        self.d11 = -0.7225
        self.d22 = -0.8612
        self.d23 = -0.1079
        self.d32 = 0.1052
        self.d33 = -1.9

        self.M_RB = np.array([
            [self.m, 0, 0],
            [0, self.m, self.m * self.xg],
            [0, self.m * self.xg, self.Iz]
        ])

        self.M_A = np.array([
            [-self.Xu, 0, 0],
            [0, -self.Yv, -self.Yr],
            [0, -self.Yr, -self.Nr]
        ])

        self.M = self.M_RB + self.M_A
        self.MI = np.linalg.inv(self.M)

        self.D = np.array([
            [-self.d11, 0, 0],
            [0, -self.d22, -self.d23],
            [0, -self.d32, -self.d33]
        ])

        self.max_v = np.array([1, 1, 30 * math.pi / 180])
        self.min_v = -self.max_v
        self.max_u = np.array([2, 1, 1.5])
        self.min_u = -self.max_u

        self.num_u = 3
        self.num_state = 6
        self.width = 1.255
        self.d_Safe = 1.67 / 2 / 1.414
        self.bd_Safe = 0.29 / 1.414

        Iu = np.eye(self.num_u)
        Zu = np.zeros((self.num_u, self.num_u))
        self.A0 = np.block([[Iu, Iu], [Zu, Iu]])
        self.B0 = np.block([[Zu], [self.MI]])
        self.C0 = np.block([Iu, Zu])
        # print(self.A0, self.B0, self.C0)

        # 航行相关参数参数
        self.gamma = 5
        self.steps = 10
        self.v_plan = 0.8 # 规划航速
        self.ts = 1 # 离散化时间间隔
        Alpha = 5 * np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 5]
        ])
        self.Alpha =  np.kron(np.eye(self.steps), Alpha)
        self.beta = 10
        self.num_gama = 0
        # self.num_input = self.num_gama + self.num_u
        self.r = self.steps
        self.eff_tau_min = 0.8178 / 2
        self.eff_tau_max = 1.0717 / 2
        self.Wvc = 0
        self.wsfc = 50 # fuel efficiency

        # 路径
        self.p_begin = np.array([]) # 航迹起点
        self.p_end = np.array([]) # 航迹终点
        self._rough_path = np.array([[]]) # 初始规划航迹
        self.delica_path = np.array([[]]) # 平滑后的航迹   

        # 优化建模相关参数
        dim = 2
        self.num_eco_slack = 2  # 为保证主机输出在经济范围而引入的松弛约束变量
        self.num_slackE = 0
        self.num_tau_u = 1
        self.num_ts = 0
        self.num_Q = dim * self.num_ts
        self.num_input = self.num_gama + self.num_u + self.num_eco_slack + 3 * self.num_Q
        self.u0 = np.zeros(self.num_input * self.steps)
        self.x_et = np.zeros(self.num_state * self.steps)

        select_mat = Struct()
        select_mat.v = np.block([Zu, Iu])

        select_mat.u = np.block([
            np.zeros((self.num_u, self.num_gama)),
            Iu,
            np.zeros((self.num_u, self.num_eco_slack)), 
            np.zeros((self.num_u, 3 * self.num_Q)), 
            np.zeros((self.num_u, self.num_slackE))
        ])

        select_mat.r = np.block([
            np.zeros((self.num_Q, self.num_gama + self.num_u)),
            np.zeros((self.num_Q, self.num_eco_slack)), 
            np.eye(self.num_Q),
            np.zeros((self.num_Q, 2 * self.num_Q)), 
            np.zeros((self.num_Q, self.num_slackE))
        ])

        select_mat.s = np.block([
            np.zeros((self.num_tau_u, self.num_gama + self.num_u)), 
            np.zeros(self.num_tau_u), 
            np.eye(self.num_tau_u),  
            np.zeros((self.num_tau_u, 3 * self.num_Q)), 
            np.zeros((self.num_tau_u, self.num_slackE))
        ])

        select_mat.tau_u = np.block([
            np.eye(self.num_tau_u),
            np.zeros((self.num_tau_u, self.num_gama + self.num_u)),
            np.zeros(self.num_tau_u),
            np.zeros((self.num_tau_u, 3 * self.num_Q)),
            np.zeros((self.num_tau_u, self.num_slackE))
        ])

        Is = np.eye(self.steps)
        select_mat.vt = np.kron(Is, select_mat.v)
        select_mat.ut = np.kron(Is, select_mat.u)
        select_mat.rt = np.kron(Is, select_mat.r)
        select_mat.st = np.kron(Is, select_mat.s)
        select_mat.tau_ut = np.kron(Is, select_mat.tau_u)
        select_mat.surge = np.kron(Is, np.array([1, 0, 0]))
        select_mat.position = np.kron(Is, np.array([[1, 0, 0], [0, 1, 0]]))
        select_mat.heading = np.kron(Is, np.array([0, 0, 1]))
        select_mat.sum_xy = np.kron(Is, np.array([1, 1]))

        self.select = select_mat

        self.A = self.A0.copy()
        self.B = np.dot(self.B0, select_mat.u)
        self.C = self.C0.copy()
        self.Ct = np.kron(Is, self.C)
        self.QC = self.C0[0 : 2, :]
        self.QCt = np.kron(Is, self.QC)

        self.L3 = np.block([
            np.zeros((self.num_tau_u, 2)),
            np.ones((self.num_tau_u, 1)),
            np.zeros((self.num_tau_u, self.num_input - 3))
        ])
        self.L3t = np.kron(Is, self.L3)

        lb = np.block([
            -np.inf * np.ones((1, self.num_gama)),
            self.min_u, 
            np.array([0, self.eff_tau_min]), 
            -10 * np.ones((1, self.num_Q)),
            np.zeros((1, 2 * self.num_Q))
        ])
        ub = np.block([
            np.inf * np.ones((1, self.num_gama)),
            self.max_u,
            np.array([2, self.eff_tau_max]), 
            10 * np.ones((1, self.num_Q)), 
            np.ones((1, 2 * self.num_Q))
        ])
        self.lbt = np.matlib.repmat(np.transpose(lb), self.steps, 1).T[0, :]
        self.ubt = np.matlib.repmat(np.transpose(ub), self.steps, 1).T[0, :]
    
    @property
    def rough_path(self):
        return self._rough_path;
    
    @rough_path.setter
    def rough_path(self, value):
        self._rough_path = value
        path.gen_path(self)# 在每次设置规划航迹时，自动完成航迹细分、生成参考状态序列
