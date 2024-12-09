import os

import numpy as np

from codes import LogWriterCode


class LogWriter:
    def __init__(self, name_folder_for_save="", need_show=False, need_save=False):
        self.need_show = need_show
        self.need_save = need_save
        self.base_dir = os.path.abspath(os.path.join(".", f"Data/{name_folder_for_save}"))
        os.makedirs(self.base_dir, exist_ok=True)

    def _save(self, stmt: list[str], filename: str, code):
        path = os.path.join(self.base_dir, code)
        os.makedirs(path, exist_ok=True)
        # Открываем файл с явной кодировкой UTF-8
        with open(os.path.join(path, f"{filename}.txt"), "a", encoding="utf-8") as file:
            file.writelines(stmt)
        print(f"Файл {filename} сохранен")

    def _matrix_and_vector_latexlog(self, A, b):
        lines = []
        # Начало LaTeX конструкции для матрицы
        lines.append("\\begin{equation}\n")
        lines.append("\t\\mathbf{A} = \\begin{pmatrix}\n")
        # Преобразуем каждую строку матрицы в формат LaTeX и добавляем в список
        for row in A:
            row_str = " & ".join(f"[{item.a}, {item.b}]" for item in row) + " \\\\\n"
            lines.append("\t\t" + row_str)
        # Закрываем матрицу
        lines.append("\t\\end{pmatrix}")
        # Преобразуем вектор b в LaTeX формат и добавляем его к уравнению
        b_str = " \\\\ ".join(f"[{item.a}, {item.b}]" for item in b)
        lines.append("\\quad \n\t\\mathbf{b} = \\begin{pmatrix}\n" + "\t\t" + b_str + " \n\t\\end{pmatrix}")
        # Закрываем конструкцию уравнения
        lines.append("\n\\end{equation}\n")
        return lines

    @staticmethod
    def _matrix_and_vector_consolelog(A, b):
        # Обрабатываем каждый элемент как строку
        print("A = \n" + "[" + "\n".join([" ".join(str(item) for item in row) for row in A]) + "]")
        print(f"b = [{', '.join(str(item) for item in b)}]")

    def _prepare_for_latex_save_solve_info(self, tol_max, argmax, envs, stmt):
        """Генерация LaTeX форматированного текста для результатов расчета."""
        lines = ["\\begin{equation}\n"]
        lines.append(f"\tTol_{{max}} = {tol_max:.3g}\n")
        lines.append("\\end{equation}\n")

        # Добавляем аргмакс в виде вектора
        lines.append("\\begin{equation}\n")
        argmax_str = " \\\\\n\t\t\t".join(f"{np.round(item, 3)[0]}" for item in argmax)
        lines.append("\t\\text Arg_{max} =\n\t\t" + "\\begin{pmatrix}\n\t\t\t" + argmax_str + "\n\t\t\\end{pmatrix}")
        lines.append("\n\\end{equation}\n")
        # Добавляем envs как таблицу
        lines.append("\\begin{equation}\n")
        envs_str = "\n\t\t\t".join(" & ".join(f"{np.round(item, 3)}" for item in row) + " \\\\" for row in envs)
        lines.append("\t\\text Envs =\n\t\t" + "\\begin{pmatrix}\n\t\t\t" + envs_str + "\n\t\t\\end{pmatrix}")
        lines.append("\n\\end{equation}\n")
        # Парсинг stmt для добавления информации по итерациям в формате LaTeX
        lines.append("\\begin{equation}\n")
        lines.append("\t\\begin{array}{cccc}\n")
        lines.append("\t\tIter & Tol(x) & Tol(xx) & TotalSteps \\\\\\hline\n")
        for iter_num, data in stmt.items():
            lines.append(f"\t\t\t{iter_num} & {data['Tol(x)']:.3f} & {data['Tol(xx)']:.3f} & {data['TotalSteps']} \\\\\n")
        lines.append("\t\\end{array}\n")
        lines.append("\\end{equation}\n")

        return lines

    # Метод для логгирования в консоль результатов расчета
    def _solve_info_intolog(self, tol_max, argmax, envs, stmt):
        res = []
        res.append(f"Tol_max = {tol_max}\n")
        res.append("Arg_max = [" + ", ".join(f"{np.round(item, 3)}" for item in argmax) + "]\n")

        # Добавление envs как строкового вывода таблицы
        res.append("Envs:\n")
        res.extend(" | ".join(f"{np.round(item, 3)}" for item in row) + "\n" for row in envs)

        # Парсинг stmt для консольного вывода информации по итерациям
        res.append("Iteration Info:\n")
        for iter_num, data in stmt.items():
            res.append(f"Iter {iter_num}: Tol(x)={data['Tol(x)']:.3f}, Tol(xx)={data['Tol(xx)']:.3f}, "
                       f"StepIdx={data['StepIdx']}, TotalSteps={data['TotalSteps']}\n")

        return res

    def log(self, name_test, code: LogWriterCode, **kwargs):
        try:
            if code == LogWriterCode.WRITEMATRIX:
                # Получаем матрицу и вектор из kwargs и записываем в консоль
                A = kwargs.get("A")
                b = kwargs.get("b")
                if A is None or b is None:
                    raise ValueError("Отсутствуют обязательные аргументы 'A' и/или 'b' для WRITEMATRIX.")

                LogWriter._matrix_and_vector_consolelog(A, b)
                if self.need_save:
                    self._save(
                        stmt=self._matrix_and_vector_latexlog(A, b),
                        filename=f"{name_test}",
                        code=code
                    )
            elif code == LogWriterCode.WRITESOLV:
                # Извлекаем данные из аргумента "info" и передаем их в функции
                info = kwargs.get("info")
                if not info or len(info) < 4:
                    raise ValueError("Отсутствует необходимая информация для WRITESOLV.")

                tol_max, argmax, envs, stmt = info
                if self.need_show:
                    print("Результаты решения:")
                    for line in self._solve_info_intolog(tol_max, argmax, envs, stmt):
                        print(line)
                if self.need_save:
                    self._save(
                        stmt=self._prepare_for_latex_save_solve_info(tol_max, argmax, envs, stmt),
                        filename=f"{name_test}",
                        code=code
                    )
            else:
                print("Неизвестный код операции.")

        except KeyError as e:
            print(f"Ошибка: Отсутствует ключевой аргумент - {e}")
            raise
        except TypeError as e:
            print(f"Ошибка: Неверный тип аргумента - {e}")
            raise
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            raise
