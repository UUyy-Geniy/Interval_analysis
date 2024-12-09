import numpy as np
from numpy.linalg import svd, lstsq, norm
from numpy import (size, all, newaxis, ones, ceil, any, abs, maximum, min, argmin, max, zeros, eye, finfo, mod, roll,
                   sum, c_, arange, sort, argsort)

# Функция для определения разрешимости задачи с интервальной линейной системой
def tolsolvty(infA, supA, infb, supb, *varargin):
    # Переменная для хранения логов по каждой итерации в виде словаря
    stmt = {}

    # Определение размеров матриц
    mi, ni = size(infA, 0), size(infA, 1)
    ms, ns = size(supA, 0), size(supA, 1)

    # Проверка размеров матриц
    if mi != ms or ni != ns:
        raise ValueError("Ошибка: несоответствие размеров матриц infA и supA.")

    m, n = ms, ns

    # Проверка векторов и согласованности их размеров
    if size(infb, 0) != size(supb, 0) or size(infb, 0) != m:
        raise ValueError("Ошибка: размер матриц не совпадает с размером векторов.")

    if not all(infA <= supA):
        raise ValueError("Ошибка: неверные интервальные элементы в матрице (infA должен быть <= supA).")

    if not all(infb <= supb):
        raise ValueError("Ошибка: неверные интервальные элементы в векторе (infb должен быть <= supb).")

    # Параметры по умолчанию
    maxitn = 2000
    nsims = 30
    epsf = 1.e-6
    epsx = 1.e-6
    epsg = 1.e-6
    alpha = 2.3
    hs = 1.0
    nh = 3
    q1, q2 = 0.9, 1.1
    iprn = 1
    weight = ones((m, 1))

    # Переопределение параметров из аргументов
    nargin = 4 + len(varargin)
    if nargin >= 5:
        iprn = ceil(varargin[0])
        if nargin >= 6:
            weight = varargin[1]
            if size(weight, 0) != m:
                raise ValueError("Ошибка: количество весов не соответствует размеру матрицы.")
            if any(weight <= 0):
                raise ValueError("Ошибка: веса должны быть положительными.")
            if nargin >= 7:
                epsf = varargin[2]
                if nargin >= 8:
                    epsx = varargin[3]
                    if nargin >= 9:
                        epsg = varargin[4]
                        if nargin >= 10:
                            maxitn = varargin[5]

    def calcfg(x):
        """Вычисляет значение функционала и градиента в точке x."""
        absx = abs(x)
        Ac_x = Ac @ x
        Ar_absx = Ar @ absx
        infs = bc - (Ac_x + Ar_absx)
        sups = bc - (Ac_x - Ar_absx)
        tt = weight * (br - maximum(abs(infs), abs(sups)))
        f, mc = min(tt), argmin(tt)

        # Вычисление градиента
        infA_mc = infA[[mc], :].conj().T
        supA_mc = supA[[mc], :].conj().T
        dl = infA_mc * (x < 0) + supA_mc * (x >= 0)
        ds = supA_mc * (x < 0) + infA_mc * (x >= 0)
        g = -weight[mc, 0] * dl if -infs[mc, 0] > sups[mc, 0] else weight[mc, 0] * ds
        return f, g, tt

    # Подготовка матриц для расчета
    Ac = 0.5 * (infA + supA)
    Ar = 0.5 * (supA - infA)
    bc = 0.5 * (infb + supb)
    br = 0.5 * (supb - infb)

    # Разложение и проверка на согласованность
    sv = svd(Ac, compute_uv=False)[:, newaxis]
    x = lstsq(Ac, bc, rcond=None)[0] if (min(sv) != 0 and max(sv) / min(sv) < 1.e+12) else zeros((n, 1))

    B = eye(n, n)  # Матрица преобразования
    vf = finfo(float).max * ones((nsims, 1))  # Отслеживание значений функции
    [f, g0, tt] = calcfg(x)
    ff, xx = f, x  # Инициализация значений оптимизации
    cal, ncals = 1, 1

    stmt[0] = {'Tol(x)': f, 'Tol(xx)': ff, 'StepIdx': cal, 'TotalSteps': ncals}

    for itn in range(1, maxitn + 1):
        # Адаптация шага и проверка на сходимость
        vf[nsims - 1, 0] = ff
        if norm(g0) < epsg:
            ccode = 2
            break
        g1 = B.conj().T @ g0
        g = B @ g1 / norm(g1)
        normg = norm(g)

        r, cal, deltax, ccode = 1, 0, 0, 0
        while r > 0 and cal <= 500:
            cal += 1
            x += hs * g
            deltax += hs * normg
            f, g1, tt = calcfg(x)
            if f > ff:
                ff, xx = f, x

            if mod(cal, nh) == 0:
                hs *= q2
            r = g.conj().T @ g1

        if cal > 500:
            ccode = 5
            break

        if cal == 1:
            hs *= q1
        ncals += cal
        if itn == iprn:
            stmt[itn] = {'Tol(x)': f, 'Tol(xx)': ff, 'StepIdx': cal, 'TotalSteps': ncals}
            iprn += iprn
        if deltax < epsx:
            ccode = 3
            break

        dg = B.conj().T @ (g1 - g0)
        xi = dg / norm(dg)
        B += (1. / alpha - 1.) * (B @ xi) @ xi.conj().T
        g0 = g1

        vf = roll(vf, 1)
        vf[0, 0] = abs(ff - vf[0, 0])
        deltaf = sum(vf) / abs(ff) if abs(ff) > 1 else sum(vf)
        if deltaf < epsf:
            ccode = 1
            break
        ccode = 4

    tolmax, argmax = ff, xx
    tt = c_[arange(1, m + 1)[newaxis].conj().T, tt]
    z, ind = sort(tt[:, [1]], 0), argsort(tt[:, [1]], 0)
    envs = tt[ind[:, 0], :]

    if iprn > 0 and mod(itn, iprn) != 0:
        stmt[itn] = {'Tol(x)': f, 'Tol(xx)': ff, 'StepIdx': cal, 'TotalSteps': ncals}

    return tolmax, argmax, envs, ccode, stmt
