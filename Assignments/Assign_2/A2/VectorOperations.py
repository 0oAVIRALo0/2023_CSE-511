from m5.params import *
from m5.SimObject import SimObject

class VectorOperations(SimObject):
    type = 'VectorOperations'
    cxx_header = "/home/monsoon2023/aviral21029/gem5/src/learning_gem5/A2/vector_operations.hh"

    waitingTIME = Param.Latency("Time before firing the event!")

    cxx_class = "gem5::VectorOperations"
