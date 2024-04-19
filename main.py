import random
import matplotlib.pyplot as plt
import math as mt
from datetime import datetime


def distance(x1, y1, x2, y2):
    return mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


M = 2
N = 1
mm = 1
nn = 1
INF = 2 ** 31 - 1

M_TYPE = 0
N_TYPE = 1
# random.seed(1)

n = M + N

v1 = []
points = {}
count = M
for i in range(n):
    if count > 0:
        points[i] = (random.randint(1, 10), random.randint(1, 10), M_TYPE)
        count = count - 1
    else:
        points[i] = (random.randint(1, 10), random.randint(1, 10), N_TYPE)

input_matrix = []
for i, vi in points.items():
    m1 = []
    for j, vj in points.items():
        if i == j:
            m1.append(INF)
        else:
            m1.append(int(distance(vi[0], vi[1], vj[0], vj[1])))
            v1.append([i, j, int(distance(vi[0], vi[1], vj[0], vj[1]))])
    input_matrix.append(m1.copy())


# -----------------------------------------------------------------
def tsp(input_matrix):
    n = len(input_matrix)
    # Генерация служебных массивов
    s = (1 << (n - 1)) - 1
    path = [0] * s
    local_sum = [0] * s

    for i in range(s):
        path[i] = [0] * (n - 1)
        local_sum[i] = [-1] * (n - 1)
    m = [n - 1, input_matrix.copy(), path, local_sum, mm, nn]

    sum_path = INF
    for i in range(m[0]):
        index = 1 << i
        if s & index != 0:
            if points[i][2] == M_TYPE:
                m[4] -= 1
            else:
                m[5] -= 1
            if m[4] > 0 or m[5] > 0:
                sum_temp = tsp_next(m, s ^ index, i) + m[1][i + 1][0]
                if sum_temp < sum_path:
                    sum_path = sum_temp
                    m[2][0][0] = i + 1

    m[3][0][0] = sum_path

    # Вывод оптимального пути
    res = []
    init_point = int(path[0][0])
    res.append(init_point)
    s = ((1 << m[0]) - 1) ^ (1 << init_point - 1)
    counter = 0
    for i in range(1, m[0]):
        init_point = int(path[s][init_point - 1])
        res.append(init_point)
        s = s ^ (1 << init_point - 1)
        counter += 1
        if counter == mm + nn:
            break
    res.append(0)
    return [sum_path, res]


# -----------------------------------------------------------------
def tsp_next(m, s, init_point):
    if m[3][s][init_point] != -1:
        return m[3][s][init_point]
    if s == 0:
        return m[1][0][init_point + 1]
    if m[4] <= 0 and m[5] <= 0:
        return m[1][0][init_point + 1]
    sum_path = INF
    for i in range(m[0]):
        index = 1 << i
        if s & index != 0:
            if points[i][2] == M_TYPE:
                m[4] -= 1
            else:
                m[5] -= 1
            sum_temp = tsp_next(m, s ^ index, i) + m[1][i + 1][init_point + 1]
            if sum_temp < sum_path:
                sum_path = sum_temp
                m[2][s][init_point] = i + 1
            if points[i][2] == M_TYPE:
                m[4] += 1
            else:
                m[5] += 1

    m[3][s][init_point] = sum_path

    return sum_path


# -----------------------------------------------------------------
# Расчёт минимальной дистанции
start_time = datetime.now()
res = tsp(input_matrix)
print(datetime.now() - start_time)
print(res)
