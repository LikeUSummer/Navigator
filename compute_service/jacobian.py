import numpy as np

def jacobian(ship):
    m11=ship.M[0, 0]
    m22=ship.M[1, 1]
    m23=ship.M[1, 2]
    m32=ship.M[2, 1]
    m33=ship.M[2, 2]

    u=ship.x_e[3]
    v=ship.x_e[4]
    r=ship.x_e[5]
    psi=ship.x_e[2]

    d11=ship.D[0, 0]
    d22=ship.D[1, 1]
    d23=ship.D[1, 2]
    d32=ship.D[2, 1]
    d33=ship.D[2, 2]
    c = np.cos(psi)
    s = np.sin(psi)

    return np.array([
        [0, 0, -v * c - u * s, c, -s, 0], 
        [0, 0, u * c - v * s, s, c, 0], 
        [0, 0, 0, 0, 0, 1], 
        [0, 0, 0, 
            -d11 / m11, 
            -(r * (ship.Yv - ship.m)) / m11, 
            -(ship.Yr * r + ship.Yv * v - ship.m * v - ship.m * r * ship.xg) / m11 - (r * (ship.Yr - ship.m * ship.xg)) / m11
        ],
        [0, 0, 0, 
            (r * (ship.Xu * m33 - ship.m * m33)) / (m22 * m33 - m23 * m32) -
                (m23 * (ship.Yr * r + ship.Yv * v - ship.m * v - ship.m * r * ship.xg)) /
                (m22 * m33 - m23 * m32) + (v * (ship.Xu * m23 - ship.m * m23)) / (m22 * m33 - m23 * m32), 
            -(d22 * m33 - d32 * m23 - ship.Xu * m23 * u + ship.m * m23 * u) /
                (m22 * m33 - m23 * m32) - (m23 * u * (ship.Yv - ship.m)) / (m22 * m33 - m23 * m32), 
            -(d23 * m33 - d33 * m23 - ship.Xu * m33 * u + ship.m * m33 * u) /
                (m22 * m33 - m23 * m32) - (m23 * u * (ship.Yr - ship.m * ship.xg)) / (m22 * m33 - m23 * m32)
        ],
        [0, 0, 0, 
            (ship.Yr * m22 * r + ship.Yv * m22 * v - ship.m * m22 * v - ship.m * m22 * r * ship.xg) /
                (m22 * m33 - m23 * m32) - (r * (ship.Xu * m32 - ship.m * m32)) /
                (m22 * m33 - m23 * m32) - (v * (ship.Xu * m22 - ship.m * m22)) / (m22 * m33 - m23 * m32), 
            (d22 * m32 - d32 * m22 - ship.Xu * m22 * u + ship.m * m22 * u) / (m22 * m33 - m23 * m32) +
                (u * (ship.Yv * m22 - ship.m * m22)) / (m22 * m33 - m23 * m32), 
            (d23 * m32 - d33 * m22 - ship.Xu * m32 * u + ship.m * m32 * u) / (m22 * m33 - m23 * m32) +
                (u * (ship.Yr * m22 - ship.m * m22 * ship.xg)) / (m22 * m33 - m23 * m32)
        ]
    ])

#测试jacobian矩阵
#ship.x_e = [0, 1, 0.5, 1, -1, 2]
#print(jacobian(ship))
