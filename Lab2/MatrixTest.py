import copy

from log_writer import LogWriter, LogWriterCode
from drawer import Drawer, DrawCode
import tools as t
from codes import TestCode


class MatrixTest:
    def __init__(self, A, b, log_writer=LogWriter(), drawer=Drawer()):
        self.A = copy.deepcopy(A)
        self.b = copy.deepcopy(b)
        self.log_writer = log_writer
        self.drawer = drawer
        self.test_exp = {TestCode.ACORRECTION: t.A_correction,
                         TestCode.ABCORRECTION: t.Ab_correction,
                         TestCode.BCORRECTION: t.b_correction}
        log_writer.log(name_test="Init_Matrix_Info", code=LogWriterCode.WRITEMATRIX, A=A, b=b)
        log_writer.log(name_test=f"Init_info", code=LogWriterCode.WRITESOLV, info=t.solve(self.A, self.b))
        _, max_x, max_Tol = t.emptinessTol(self.A, self.b)
        drawer.draw(name_test=f"Init_info", code=DrawCode.PLOTTOLSET, A=self.A, b=self.b,
                    max_x=max_x, max_Tol=max_Tol, title_name="Initial")
        self.drawer.draw(name_test="Init_info", code=DrawCode.PLOTTOLMESH,
                         A=self.A, b=self.b,
                         max_x=max_x, max_Tol=max_Tol,
                         title_name=f"Init")

    def test(self, code: TestCode):
        A_internal, b_internal = copy.deepcopy(self.A), copy.deepcopy(self.b)

        A_internal, b_internal = self.test_exp[code](A_internal, b_internal)
        _, max_x, max_Tol = t.emptinessTol(A_internal, b_internal)

        self.log_writer.log(name_test=f"Matrix_Info_with_{code}",
                            code=LogWriterCode.WRITEMATRIX,
                            A=A_internal, b=b_internal)

        self.drawer.draw(name_test=code, code=DrawCode.PLOTTOLSET,
                         A=A_internal, b=b_internal,
                         max_x=max_x, max_Tol=max_Tol,
                         title_name=f"After_{code}")

        self.drawer.draw(name_test=code, code=DrawCode.PLOTTOLMESH,
                         A=A_internal, b=b_internal,
                         max_x=max_x, max_Tol=max_Tol,
                         title_name=f"After_{code}")

        self.log_writer.log(name_test=f"After_{code}", code=LogWriterCode.WRITESOLV,
                            info=t.solve(A_internal, b_internal))
