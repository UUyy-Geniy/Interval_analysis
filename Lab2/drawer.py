from codes import DrawCode
from tools import draw_Tol, draw_tol_set

import os
import matplotlib.pyplot as plt


class Drawer:
    def __init__(self, name_folder_for_save="", need_show=False, need_save=False):
        self.need_show = need_show
        self.need_save = need_save
        self.base_dir = os.path.abspath(os.path.join(".", f"graphics/{name_folder_for_save}"))
        self.drawer_map_tool = {
            DrawCode.PLOTTOLSET: draw_tol_set,
            DrawCode.PLOTTOLMESH: draw_Tol,
        }
        os.makedirs(self.base_dir, exist_ok=True)

    def draw(self, name_test, code: DrawCode, **kwargs):
        try:
            path = os.path.join(self.base_dir, code, name_test)
            os.makedirs(path, exist_ok=True)
            self.drawer_map_tool[code](path=path, need_save=self.need_save,
                                       need_show=self.need_show,
                                       **kwargs)

        except KeyError as e:
            print(f"Ошибка: Некорректный код графика - {e}")
            raise
        except TypeError as e:
            print(f"Ошибка: Неверный тип аргументов для функции рисования - {e}")
            raise
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            raise
