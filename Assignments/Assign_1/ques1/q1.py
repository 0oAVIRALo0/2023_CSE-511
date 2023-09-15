# import the m5 (gem5) library created when gem5 is built
import m5

# import all of the SimObjects
from m5.objects import *

from caches import *
import argparse

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("binary", default="", nargs="?", type=str,
                    help="Path to the binary to execute.")
parser.add_argument("--l1i_size",
                    help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size",
                    help="L1 data cache size. Default: Default: 16kB.")
parser.add_argument("--l2_size",
                    help="L2 cache size. Default: 256kB.")
parser.add_argument("--l1i_assoc", type=int,
                    help="L1 instruction cache associativity.")
parser.add_argument("--l1d_assoc", type=int,
                    help="L1 data cache associativity.")
parser.add_argument("--l2_assoc", type=int,
                    help="L2 cache associativity.")
parser.add_argument("--l1i_latency",
                    help="L1 instruction cache latency.")
parser.add_argument("--l1d_latency",
                    help="L1 data cache latency.")
parser.add_argument("--l2_latency",
                    help="L2 cache latency.")

options = parser.parse_args()

# create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range

# Create a simple CPU
# You can use ISA-specific CPU models for different workloads:
# `RiscvTimingSimpleCPU`, `ArmTimingSimpleCPU`.
system.cpu = X86TimingSimpleCPU()

# Creating L1 caches
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

# connect the caches to the CPU ports with the helper function we created
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)


# We can’t directly connect the L1 caches to the L2 cache since the L2 cache only expects a single port to connect to it. 
# Therefore, we need to create an L2 bus to connect our L1 caches to the L2 cache. 
# The, we can use our helper function to connect the L1 caches to the L2 bus.
system.l2bus = L2XBar()
# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Next, we can create our L2 cache and connect it to the L2 bus and the memory bus.
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

# Create a memory bus
system.membus = SystemXBar()
# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)

# Create a memory bus, a system crossbar, in this case
# system.membus = SystemXBar()

# Hook the CPU ports up to the membus
# system.cpu.icache_port = system.membus.cpu_side_ports        REMOVE
# system.cpu.dcache_port = system.membus.cpu_side_ports        REMOVE

# create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()

# For X86 only we make sure the interrupts care connect to memory.
# Note: these are directly connected to the memory bus and are not cached.
# For other ISA you should remove the following three lines.
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports



# Here we set the X86 "hello world" binary. With other ISAs you must specify
# workloads compiled to those ISAs. Other "hello world" binaries for other ISAs
# can be found in "tests/test-progs/hello".
thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../../",
    "tests/test-progs/hello/bin/x86/linux/hello",
)

system.workload = SEWorkload.init_compatible(binary)

# Create a process for a simple "Hello World" application
process = Process()
# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = ['/home/monsoon2023/aviral21029/gem5/configs/mibench/automotive/qsort/qsort_small', '/home/monsoon2023/aviral21029/gem5/configs/mibench/automotive/qsort/input_small.dat']
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))
