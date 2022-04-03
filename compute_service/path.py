import numpy as np

# 根据始末点的位置、速度和时间，为路径插值控制生成所需的加速度线性函数（系数b, m）
def kine_interpolation(p, v, t):
    # a(t) = f(t) = b + m(t - t0)
    dt = t[1] - t[0]
    dp = p[1, :] - p[0, :]
    dv = v[1, :] - v[0, :]
    A = np.mat([[dt, dt**2 / 2], [dt**2 / 2, pow(dt, 3) / 6]])
    B = np.vstack((dv, dp - v[0, :] * dt))
    C = A.I * B
    b = np.asarray(C)[0, :]
    m = np.asarray(C)[1, :]
    return b, m

# 根据始末点的位置、速度和时间，计算插值路径点及对应速度
def smooth_line(p, v, t, n):
    ts = np.linspace(t[0], t[1], n) 
    b, m = kine_interpolation(p, v, t)

    locs_x = p[0, 0] + v[0, 0] * (ts - t[0]) + 1 / 2 * b[0] * (ts - t[0]) * (ts - t[0]) + 1 / 6 * m[0] * (ts - t[0]) * (ts - t[0]) * (ts - t[0])
    locs_y = p[0, 1] + v[0, 1] * (ts - t[0]) + 1 / 2 * b[1] * (ts - t[0]) * (ts - t[0]) + 1 / 6 * m[1] * (ts - t[0]) * (ts - t[0]) * (ts - t[0])

    vels_x = v[0, 0] + b[0] * (ts - t[0]) + m[0] / 2 * ((ts - t[0]) * (ts - t[0]))
    vels_y = v[0, 1] + b[1] * (ts - t[0]) + m[1] / 2 * ((ts - t[0]) * (ts - t[0]))

    locs = np.block([[locs_x], [locs_y]]).T
    vels = np.block([[vels_x], [vels_y]]).T

    return locs, vels

# 测试路径生成模块
# import matplotlib.pyplot as plt
# p, v = gen_path(np.array([[1, 2], [8, 5]]), np.array([[1, 1], [0.5, 0.1]]), [0.5, 3.5], 10)
# print(p, v)
# plt.plot(p[:, 0], p[:, 1])
# plt.title('gen_path')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()

# 笛卡尔坐标转极坐标，支持传入数组
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

# 根据规划航迹生成光滑的参考航迹
def gen_path(ship):
    # 预处理
    points = ship.rough_path
    ship.p_begin = points[0, :]
    ship.p_end = points[-1, :]
    pt =  points[-2, :]
    pt = ship.p_end + ship.p_end - pt # 延伸最后一段路径，便于尾段的优化计算
    rough_path = np.vstack((points, pt))
    # 细分航迹
    n = rough_path.shape[0]
    div_path = []
    div = np.array([[]])
    for i in range(n - 1):
        if i == 0:
            begin_point = rough_path[i, :]
        else:
            begin_point = div[-1, :]
        line = rough_path[i + 1, :] - begin_point
        line_len = np.linalg.norm(line)
        v = ship.v_plan * line / line_len
        t = np.round(line_len / ship.v_plan).astype(int)
        ts = np.array([k for k in range(1, t + 1)])
        if t != 0:
            div = begin_point + v * np.transpose([ts])
        else:
            print("路径分段模块产生错误")
            quit(code = 0)
        div_path.append(div)

    # 平滑航迹，生成参考轨迹点
    ship.delica_path = np.array([ship.p_begin])
    for i in range(len(div_path) - 1):
        cp = np.min([20, div_path[i].shape[0] - 1, div_path[i + 1].shape[0] - 1])

        if i == 0:
            p1 = div_path[i][-cp - 1, :]
            v1 = div_path[i][-cp, :] - div_path[i][-cp - 1, :]
        else:
            p1 = ship.delica_path[-cp - 1, :]
            v1 = ship.delica_path[-cp, :] - ship.delica_path[-cp - 1, :]
        p2 = div_path[i + 1][cp - 1, :]
        v2 = div_path[i + 1][cp, :] - div_path[i + 1][cp - 1, :]
        # print(p1, p2, v1, v2)
        ps, vs = smooth_line(np.array([p1, p2]), np.array([v1, v2]), [0, 2 * cp], 2 * cp + 1)
        if i == 0:
            ship.delica_path = np.block([[ship.delica_path], [div_path[i][0 : -cp - 1, :]], [ps], [div_path[i + 1][cp:, :]]])
        else:
            ship.delica_path = np.block([[ship.delica_path[0 : -cp - 1, :]], [ps], [div_path[i + 1][cp:, :]]])

    # 计算各点航向
    course = ship.delica_path[1:, :] - ship.delica_path[:-1, :]
    (rho, heading) = cart2pol(course[:, 0], course[:, 1])
    n = heading.shape[0]
    for i in range(1, n):
        while heading[i] - heading[i - 1] > np.pi:
            heading[i] = heading[i] - 2 * np.pi
        while heading[i] - heading[i - 1] < -np.pi:
            heading[i] = heading[i] + 2 * np.pi
    heading = np.append(heading, heading[-1]) # 重复追加末尾元素，使航向数量和航迹点匹配
    ship.ref_state = np.block([ship.delica_path, np.transpose([heading])])
