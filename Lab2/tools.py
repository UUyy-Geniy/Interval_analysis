import copy
import os

import numpy as np
import intvalpy as ip
import matplotlib.pyplot as plt

from solver import tolsolvty

ip.precision.extendedPrecisionQ = False


def emptinessTol(A, b):
    maxTol = ip.linear.Tol.maximize(A, b)  # searchMaxTol
    if maxTol[1] < 0:
        return True, maxTol[0], maxTol[1]
    else:
        return False, maxTol[0], maxTol[1]


def b_correction(A, b, step=5):
    mid = ip.mid(b)
    new_rad = step * ip.rad(b)
    new_b = [[mid[i] - new_rad[i], mid[i] + new_rad[i]] for i in range(len(mid))]

    return A, ip.Interval(new_b)


def A_correction(A, b, step=5, tol_max=[1, 2]):
    cols = len(tol_max)
    rows = A.shape[0]
    delta = np.min(np.sum(abs(tol_max[j]) * ip.rad(A[i][j]) for j in range(cols)) for i in range(rows))

    mid = ip.mid(A)
    new_rad = ip.rad(A) / step
    new_A = []
    for i in range(len(mid)):
        row = []
        for j in range(len(mid[0])):
            row.append([mid[i][j] - new_rad[i][j], mid[i][j] + new_rad[i][j]])
        new_A.append(row)

    return ip.Interval(new_A), b


def Ab_correction(A, b):
    emptiness, _, _ = emptinessTol(A, b)
    new_A = copy.deepcopy(A)
    new_b = copy.deepcopy(b)

    while emptiness:
        new_A, _ = A_correction(new_A, new_b, step=2)
        emptiness, _, _ = emptinessTol(new_A, new_b)
        if not emptiness:
            break

        _, new_b = b_correction(new_A, new_b, step=2)
        emptiness, _, _ = emptinessTol(new_A, new_b)

    return new_A, new_b


def draw_Tol(A, b, max_x, max_Tol, need_save, need_show, path, **kwargs):
    title_name = kwargs.get("title_name")
    if not title_name:
        raise ValueError("Отсутствует обязательный элемент: title_name для отрисовки меша!")

    # Настройка сетки значений для x1 и x2
    grid_min, grid_max = max_x[0] - 2, max_x[0] + 2
    x_1_, x_2_ = np.mgrid[grid_min:grid_max:100j, grid_min:grid_max:100j]
    list_x_1 = np.linspace(grid_min, grid_max, 100)
    list_x_2 = np.linspace(grid_min, grid_max, 100)

    # Подготовка tol значений
    list_tol = np.zeros((100, 100))
    for idx_x1, x1 in enumerate(list_x_1):
        for idx_x2, x2 in enumerate(list_x_2):
            x = [x1, x2]
            tol_values = []
            for i in range(len(b)):
                sum_ = sum(A[i][j] * x[j] for j in range(len(x)))
                rad_b, mid_b = ip.rad(b[i]), ip.mid(b[i])
                tol = rad_b - ip.mag(mid_b - sum_)
                tol_values.append(tol)
            list_tol[idx_x1, idx_x2] = min(tol_values)

    # Генерация углов на основе max_Tol
    base_elev, base_azim = 30, 45  # Начальные углы для обзора
    angle_offsets = [(0, 0), (30, 0)]  # Смещения углов для 4 перспектив
    # Построение графика и сохранение с разных углов
    for i, (elev_offset, azim_offset) in enumerate(angle_offsets):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_1_, x_2_, list_tol, cmap="Greys")

        # Добавляем точку с максимальным значением tolerance
        ax.scatter(*max_x, max_Tol, color='red', s=50, label="Max Tol Point")
        ax.legend(loc="upper right")

        # Настройка угла обзора
        elev, azim = base_elev + elev_offset, base_azim + azim_offset
        ax.view_init(elev=elev, azim=azim)
        ax.dist = 10
        ax.set_title(f"{title_name} with angle = {elev}, {azim}")

        name = f"angle_{elev}_{azim}"

        if need_save:
            fig.savefig(f"{path}/{name}.png", bbox_inches='tight')
        if need_show:
            plt.show(fig)
        plt.close(fig)
        # Применяем изменения к фигуре перед тем, как сохранять её


def draw_tol_set(A, b, max_x, max_Tol, need_save, need_show, path, **kwargs):
    # Создаем фигуру и ось
    title_name = kwargs.get("title_name")
    if not title_name:
        raise ValueError("Отсутствует обязательный элемент: title_name для отрисовки меша!")

    # Вызов функции для построения tolerance set
    ip.IntLinIncR2(A, b, consistency="tol")

    # Добавляем точку с максимальным значением tolerance
    plt.scatter(max_x[0], max_x[1], color='red', s=100, label=f"Max Tol: {max_Tol:.2f}")
    # ax.annotate(f"({max_x[0]:.2f}, {max_x[1]:.2f})", (max_x[0], max_x[1]),
    #             textcoords="offset points", xytext=(10, 10), ha='center', fontsize=12, color='red')

    # Настройка графика
    plt.title(title_name, fontsize=16, weight='bold')
    plt.xlabel("x1", fontsize=14)
    plt.ylabel("x2", fontsize=14)
    plt.legend(loc="upper right")
    plt.grid()

    if need_save:
        plt.savefig(f"{path}/{title_name}.png", bbox_inches='tight')
    if need_show:
        plt.show()
    plt.close()






def solve(A, b):
    tol_max, argmax, envs, _, stmt = tolsolvty(infA=ip.inf(A), supA=ip.sup(A),
                                           infb=ip.inf(b).reshape(-1, 1),
                                           supb=ip.sup(b).reshape(-1, 1))
    return tol_max, argmax, envs, stmt

# emptiness_, maxX, maxTol = emptinessTol(A_, b_)
# print(emptiness_)
# draw_Tol(A_, b_, maxX, maxTol)


# A_c, b_c = Ab_correction(A_, b_)
# emptiness_, maxX, maxTol = emptinessTol(A_c, b_c)
# print(emptiness_, maxX, maxTol)

# draw_Tol(A_c, b_c, maxX, maxTol)


# new_b = b_correction(A_, b_)
# print(new_b)
# print(emptinessTol(A_, new_b))
#
# ip.IntLinIncR2(A_, new_b, consistency='tol')
# plt.scatter(1, 2)
# plt.show()
#

# new_A = A_correction(A_, b_)
# print(new_A)
# print(emptinessTol(new_A, b_))
# ip.IntLinIncR2(new_A, b_, consistency='tol')
# plt.scatter(1, 2)
# plt.show()

# print(ip.sup(b_).reshape(-1, 1))
# tolmax, argmax, envs, ccode = tolsolvty(infA=ip.inf(A_), supA=ip.sup(A_),
#                                         infb=ip.inf(b_).reshape(-1, 1), supb=ip.sup(b_).reshape(-1, 1))
#
# print(tolmax)
# print(argmax)
# print(envs)
