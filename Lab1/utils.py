import numpy as np
from interval_module import Interval
from illustrator import illustrate_matrix
import os


def get_interval_matrix(eps: float):
    return np.array([[Interval(1.05 - eps, 1.05 + eps), Interval(0.95 - eps, 0.95 + eps)],
                     [Interval(1 - eps, 1 + eps), Interval(1 - eps, 1 + eps)]])

def get_interval_matrix_new(eps: float):
    return np.array([[Interval(1.05 - eps, 1.05 + eps), Interval(0.95 - eps, 0.95 + eps)],
                     [Interval(1, 1), Interval(1, 1)]])

def print_matrix_for_latex(matrix, index=0):
    res = "\\begin{equation}\n\\text A_%d = \\begin{pmatrix}\n\t" % index
    res += "\t".join(["&".join([item.__repr__() for item in items]) + "\\\\\n" for items in matrix])
    res += "\end{pmatrix}\n\end{equation}"
    print(res)
    return res


# Нахождение максимального среднего значения в матрице
def find_max_middle(matrix):
    max_mid = -float("inf")
    for row in matrix:
        for interval in row:
            max_mid = max(max_mid, interval.mid())
    return max_mid


def determ(i, j, matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

def save_step_info(info: list[str], folder_name="fmatrix"):
    # Получаем абсолютный путь к папке, где будет сохранён файл
    base_dir = os.path.abspath(os.path.join(".", "Lab1/step_info"))
    path_info = os.path.join(base_dir, folder_name)
    
    # Создаём папку, если её не существует
    os.makedirs(path_info, exist_ok=True)
    
    # Путь к файлу
    file_path = os.path.join(path_info, f"arcticle_for_{folder_name}.txt")
    
    try:
        # Открываем файл и записываем информацию
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(info))
        print(f"Файл успешно сохранён: {file_path}")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

def generate_step_info(matrix, step_number, delta, interval, left_bound, right_bound):
    return f"$\\delta = {delta}$" + \
    f"\nNumber: {step_number}:\n{print_matrix_for_latex(matrix, step_number)}" + \
    f"\nИтоговый интервал из определителя {interval}"+\
    f"\n$\\delta \\in $ [{left_bound}, {right_bound}]"

def optimize(left, right, delta, get_matrix = get_interval_matrix, folder_name="fmatrix") -> (float, float):
    counter = 0
    counter_left = 0
    counter_right = 0
    info_steps = []
    trace = "-" * 20 + "\n" + "-" * 20
    while right - left > delta:
        c = (right + left) / 2
        counter += 1
        matrix_tmp = get_matrix(c)
        interval = determ(0, 0, matrix_tmp)
        if not 0 in interval:
            if counter_left < 2:
                step_info = generate_step_info(matrix_tmp, counter, c, interval, left_bound=left, right_bound=right)
                info_steps.append(step_info)
                print(trace + "\nСдвиг влево:\n" + trace + "\n" + step_info)
                illustrate_matrix(matrix=matrix_tmp, step_number=counter, folder_name=folder_name, delta=c)
            counter_left += 1
            left = c
        else:
            
            if counter_right < 2:
                step_info = generate_step_info(matrix_tmp, counter, c, interval, left_bound=left, right_bound=right)
                info_steps.append(step_info)
                print(trace + "\nСдвиг вправо:\n" + trace + "\n" + step_info)
                illustrate_matrix(matrix=matrix_tmp, step_number=counter, folder_name=folder_name, delta=c)
            counter_right += 1
            right = c

    info_steps.append(generate_step_info(matrix_tmp, counter, c, interval, left_bound=left, right_bound=right))
    print("-" * 20)
    print(f"$\\delta = {c}$")
    print(f"Number: {counter}:\n{print_matrix_for_latex(matrix_tmp, counter)}"
        f"\nИтоговый интервал из определителя{interval}")
    illustrate_matrix(matrix=matrix_tmp, step_number=counter, folder_name=folder_name, delta=c)

    save_step_info(info_steps, folder_name=folder_name)
    
    return right, left, counter


def determinant_optimization_new(matrix=None, delta=1e-5, get_matrix = get_interval_matrix, folder_name="fmatrix"):
    if matrix is None:
        matrix = get_interval_matrix(0)

    mid = find_max_middle(matrix)

    eps_curr = mid
    eps_left_bound = 0
    counter = 1

    eps_curr, eps_left_bound, amount = optimize(eps_left_bound, eps_curr, delta, get_matrix=get_matrix, folder_name=folder_name)

    print(f"Кол-во вызовов функции: {counter + 1}")
    return eps_curr


# Task info for research

# determinant_optimization_new(delta=1e-10, get_matrix=get_interval_matrix, folder_name="fmatrix")
determinant_optimization_new(delta=1e-10, get_matrix=get_interval_matrix_new, folder_name="smatrix")