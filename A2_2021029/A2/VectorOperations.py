from m5.params import *
from m5.SimObject import SimObject

class VectorOperations(SimObject):
    type = 'VectorOperations'
    cxx_header = "/home/monsoon2023/aviral21029/gem5/configs/A2_2021029/A2/vector_operations.hh"

    t = Param.Latency("ticks")

    cxx_class = "gem5::VectorOperations"
