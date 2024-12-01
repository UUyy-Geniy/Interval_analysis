import numpy as np
from interval_module import Interval

# Генерация интервальной матрицы 2x2
def get_interval_matrix(eps: float):
    return np.array([[Interval(1 - eps, 1 + eps), Interval(0.9 - eps, 0.9 + eps)],
                     [Interval(1.5 - eps, 1.5 + eps), Interval(1.1 - eps, 1.1 + eps)]])

# Пересечение интервалов
def intersect_intervals(ratios):
    item = ratios[0]
    for ratio in ratios[1:]:
        item = item & ratio
        if item.lower == item.upper == 0:  # Если пересечение пустое
            return None
    return item


# Проверка коллинеарности векторов
def is_scalar(v1, v2) -> bool:
    ratios = []
    for i in range(len(v1)):
        try:
            ratio = v1[i] / v2[i]
        except ZeroDivisionError:
            return False
        ratios.append(ratio)
    return intersect_intervals(ratios) is not None

def optimize(i, j, left, right, delta) -> (float, float):
    counter = 0
    while right - left > delta:
        c = (right + left) / 2
        counter += 1
        matrix_tmp = get_interval_matrix(c)

        v1, v2 = matrix_tmp[i], matrix_tmp[j]

        if not is_scalar(v1, v2):
            left = c
        else:
            right = c

        print(f"Текущие границы [{left}, {right}]")
    return right, left, counter


# Основная функция оптимизации
def determinant_optimization(matrix=None, delta=1e-5):
    if matrix is None:
        matrix = get_interval_matrix(0)

    mid = find_max_middle(matrix)
    n = len(matrix)

    eps_curr = mid * 1.7 + 15
    eps_left_bound = 0
    counter = 1
    for i in range(n):
        for j in range(i + 1, n):  # Изменил цикл, чтобы j всегда > i
            eps_curr, eps_left_bound, amount = optimize(i, j,
                                                        eps_left_bound, eps_curr, delta)
            counter += amount
    print(f"Кол-во вызовов функции: {counter + 1}")
    return eps_curr


# for eps in [1e-1, 1e-2, 1e-3, 1e-14]:
#     print(f"eps = {eps} Result = {determinant_optimization_new(delta=eps)}")