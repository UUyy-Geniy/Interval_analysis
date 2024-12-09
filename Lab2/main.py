from MatrixTest import MatrixTest, TestCode
from log_writer import LogWriter
from drawer import Drawer
import intvalpy as ip

# First Matrix
A = ip.Interval([
    [[0.65, 1.25], [0.7, 1.3]],
    [[0.75, 1.35], [0.7, 1.3]]
])
b = ip.Interval([[2.75, 3.15],
                 [2.85, 3.25]])

Test1 = MatrixTest(A, b,
                   LogWriter(need_show=False, need_save=True, name_folder_for_save="Test1"),
                   Drawer(need_show=False, need_save=True, name_folder_for_save="Test1"))

Test1.test(code=TestCode.ACORRECTION)
Test1.test(code=TestCode.BCORRECTION)
Test1.test(code=TestCode.ABCORRECTION)

# Second Matrix

A_ = ip.Interval([
    [[0.65, 1.25], [0.70, 1.3]],
    [[0.75, 1.35], [0.70, 1.3]],
    [[0.8, 1.4], [0.70, 1.3]],
    [[-0.3, 0.3], [0.70, 1.3]]
])

b_ = ip.Interval([
    [2.75, 3.15],
    [2.85, 3.25],
    [2.90, 3.3],
    [1.8, 2.2],
    ])
Test2 = MatrixTest(A_, b_,
                   LogWriter(need_show=False, need_save=True, name_folder_for_save="Test2"),
                   Drawer(need_show=False, need_save=True, name_folder_for_save="Test2"))

Test2.test(code=TestCode.ACORRECTION)
Test2.test(code=TestCode.BCORRECTION)
Test2.test(code=TestCode.ABCORRECTION)


A_ = ip.Interval([
    [[0.65, 1.25], [0.70, 1.3]],
    [[0.75, 1.35], [0.70, 1.3]],
    [[0.8, 1.4], [0.70, 1.3]]
])
b_ = ip.Interval([
    [2.75, 3.15],
    [2.85, 3.25],
    [2.90, 3.3]
    ])

Test2 = MatrixTest(A_, b_,
                   LogWriter(need_show=False, need_save=True, name_folder_for_save="Test3"),
                   Drawer(need_show=False, need_save=True, name_folder_for_save="Test3"))

Test2.test(code=TestCode.ACORRECTION)
Test2.test(code=TestCode.BCORRECTION)
Test2.test(code=TestCode.ABCORRECTION)
