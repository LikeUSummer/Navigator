from statistics import mode
from pyomo.environ import *
from pyomo.gdp import *
from pyomo.core.util import *
import numpy as np

def MIQP(H, f, A, b, lb, ub, x0):
    model = ConcreteModel()
    # 变量
    def bound(model, i):
        return (lb[i], ub[i])
    def init(model, i):
        if x0[i] < lb[i] or x0[i] > ub[i]:
            x0[i] = (lb[i] + ub[i]) / 2 # 避免越界告警
        return x0[i]
    model.x = Var(range(H.shape[0]), bounds = bound, initialize = init)

    # 根据二次型矩阵生成目标函数
    value = []
    target = 0
    for i in range(H.shape[0]):
        value.append(0)
        for j in range(H.shape[1]):
            value[i] += H[i, j] * model.x[j]
    for i in range(len(value)):
        target += 0.5 * value[i] * model.x[i] + f[i] * model.x[i]
    model.obj = Objective(expr = target, sense = minimize)

    # 约束
    def con(model, i):
        value = 0
        for j in range(A.shape[1]):
            value += A[i, j] * model.x[j]
        return (None, value, b[i])
    model.con = Constraint(range(A.shape[0]), rule = con)

    # model.pprint() # 输出模型摘要

    # 求解
    # 1、GLPK + IPOPT组合求解
    # SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt')#.write() 
    # 2、BONMIN 可求全局最优
    SolverFactory('bonmin', executable="./solvers/bonmin/bonmin.exe").solve(model)#.write() 
    # 3、SCIP 求解
    # SolverFactory('scip', executable="./solvers/scip/scipampl.exe").solve(model)#.write

    return model.obj(), np.array([model.x[i]() for i in range(H.shape[0])])

# 测试MIQP模块
# H = np.array([[1, 2], [2, 1]])
# f = np.array([1, -3])
# A = np.array([[-1, 1], [1, -3]])
# b = np.array([20, 30])
# lb = np.array([0, -10])
# ub = np.array([40, 3])
# x0 = np.array([1, 2])
# y, x = MIQP(H, f, A, b, lb, ub, x0)
# print(y, x)
