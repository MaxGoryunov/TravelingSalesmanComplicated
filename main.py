import random
import math as mt
from datetime import datetime


def distance(x1, y1, x2, y2):
    return mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


M = 8
N = 8
mm = 5
nn = 5
INF = 2 ** 31 - 1

M_TYPE = 'a'
N_TYPE = 'b'
# random.seed(1)

n = M + N

v1 = []
points = []
count = M
for i in range(n):
    if count > 0:
        points.append(((random.randint(1, 10000), random.randint(1, 10000)), M_TYPE))
        count = count - 1
    else:
        points.append(((random.randint(1, 10000), random.randint(1, 10000)), N_TYPE))

# points = [((148, 138), 'a'), ((346, 448), 'a'), ((278, 752), 'a'),
#           ((758, 39), 'a'), ((860, 750), 'a'), ((39, 952), 'a'),
#           ((514, 241), 'a'), ((637, 862), 'a'), ((85, 79), 'b'),
#           ((622, 58), 'b'), ((786, 555), 'b'), ((580, 268), 'b'),
#           ((1, 45), 'b'), ((775, 789), 'b'), ((988, 260), 'b'), ((762, 599), 'b')]


# -----------------------------------------------------------------
def tsp(points):
    n = len(points)
    results = []
    for num in range(n):
        current_points = points.copy()
        current_points[0] = points[num]
        current_points[num] = points[0]
        input_matrix = []
        for i, vi in enumerate(current_points):
            m1 = []
            for j, vj in enumerate(current_points):
                if i == j:
                    m1.append(INF)
                else:
                    m1.append(int(distance(vi[0][0], vi[0][1], vj[0][0], vj[0][1])))
                    v1.append([i, j, int(distance(vi[0][0], vi[0][1], vj[0][0], vj[0][1]))])
            input_matrix.append(m1.copy())
        # Генерация служебных массивов
        s = (1 << (n - 1)) - 1
        path = [0] * s
        local_sum = [0] * s

        for i in range(s):
            path[i] = [0] * (n - 1)
            local_sum[i] = [-1] * (n - 1)
        m = [n - 1, input_matrix.copy(), path, local_sum, mm, nn]
        sum_path = INF
        if current_points[0][1] == M_TYPE:
            m[4] -= 1
        else:
            m[5] -= 1
        for i in range(m[0]):
            index = 1 << i
            if s & index != 0:
                if current_points[i+1][1] == M_TYPE:
                    m[4] -= 1
                else:
                    m[5] -= 1
                if m[4] > 0 or m[5] > 0:
                    sum_temp = tsp_next(m, s ^ index, i, current_points) + m[1][i + 1][0]  # delete При необходимости
                    if sum_temp < sum_path:
                        sum_path = sum_temp
                        m[2][0][0] = i + 1
                if current_points[i+1][1] == M_TYPE:
                    m[4] += 1
                else:
                    m[5] += 1
        if current_points[0][1] == M_TYPE:
            m[4] += 1
        else:
            m[5] += 1
        m[3][0][0] = sum_path

        # Вывод оптимального пути
        res = []
        init_point = int(path[0][0])
        res.append(init_point)
        s = ((1 << m[0]) - 1) ^ (1 << init_point - 1)
        counter = 0
        for i in range(1, m[0]):
            counter += 1
            if counter == mm + nn - 1:
                break
            init_point = int(path[s][init_point - 1])
            res.append(init_point)
            s = s ^ (1 << init_point - 1)
        res.append(0)  #
        results.append([sum_path, res, current_points, num])

    max_res = results[0]
    counter = 0
    for i, resul in enumerate(results):
        if resul[0] < max_res[0]:
            max_res = resul
    for i, resul in enumerate(results):
        if resul[0] == max_res[0]:
            counter += 1
    for resul in results:
        print(resul)
    print(counter)
    in_0 = -1
    in_num = -1
    if 0 in max_res[1]:
        in_0 = max_res[1].index(0)
    if max_res[3] in max_res[1]:
        in_num = max_res[1].index(max_res[3])
    if in_0 != -1:
        max_res[1][in_0] = max_res[3]
    if in_num != -1:
        max_res[1][in_num] = 0
    type1 = 0
    type2 = 0
    for ind in max_res[1]:
        if points[ind][1] == M_TYPE:
            type1 += 1
        else:
            type2 += 1
    print(f"type1={type1}, type2 ={type2}")
    return [max_res[0], max_res[1]]


# -----------------------------------------------------------------
def tsp_next(m, s, init_point, current_points):
    if m[3][s][init_point] != -1:
        return m[3][s][init_point]
    if s == 0:
        return m[1][0][init_point + 1]
    if m[4] == 0 and m[5] == 0:
        return m[1][0][init_point + 1]
    if m[4] < 0 or m[5] < 0:
        return INF
    sum_path = INF
    for i in range(m[0]):
        index = 1 << i
        if s & index != 0:
            if m[4] == 0 and current_points[i + 1][1] == M_TYPE:
                continue
            if m[5] == 0 and current_points[i + 1][1] == N_TYPE:
                continue
            if current_points[i + 1][1] == M_TYPE:
                m[4] -= 1
            else:
                m[5] -= 1
            sum_temp = tsp_next(m, s ^ index, i, current_points) + m[1][i + 1][init_point + 1]
            if sum_temp < sum_path:
                sum_path = sum_temp
                m[2][s][init_point] = i + 1
            if current_points[i + 1][1] == M_TYPE:
                m[4] += 1
            else:
                m[5] += 1

    m[3][s][init_point] = sum_path

    return sum_path


# -----------------------------------------------------------------
# Расчёт минимальной дистанции
start_time = datetime.now()
res = tsp(points)
print(datetime.now() - start_time)
print(res)
# res[1].append(res[1][0])
# our_res = res[1]
# m_res = [1, 2, 7, 13, 4, 15, 10, 11, 9, 6, 1]
# dist1=0
# dist2=0
# for i in range(len(m_res)-1):
#     dist1+=distance(points[our_res[i]][0][0],points[our_res[i]][0][1],points[our_res[i+1]][0][0],points[our_res[i+1]][0][1])
#     dist2 += distance(points[m_res[i]][0][0], points[m_res[i]][0][1], points[m_res[i + 1]][0][0],
#                       points[m_res[i + 1]][0][1])
# print(f"our dist = {dist1}, Misha dist = {dist2}")