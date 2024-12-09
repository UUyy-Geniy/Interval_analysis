from enum import Enum


class StrEnum(str, Enum):
    pass


class DrawCode(StrEnum):
    PLOTTOLSET = "tolerance_set"
    PLOTTOLMESH = "tolerance_mesh"


class LogWriterCode(StrEnum):
    WRITECORRECTION = "correction_info"
    WRITESOLV = "solution_info"
    WRITEMATRIX = "init_matrix_info"


class TestCode(StrEnum):
    ACORRECTION = "acorrection"
    BCORRECTION = "bcorrection"
    ABCORRECTION = "abcorrection"
