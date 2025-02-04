import argparse

import m5
from m5.objects import (
    AddrRange,
    DDR3_1600_8x8,
    MemCtrl,
    Process,
    Root,
    SEWorkload,
    SimpleCache,
    SrcClockDomain,
    System,
    SystemXBar,
    VoltageDomain,
    X86MinorCPU,
)

# Add Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("binary", help="Binary to run", default="/u/csc368h/winter/pub/workloads/hello")
parser.add_argument("-a", "--binary_args", help="Arguments to pass to the binary", required=False)

args = parser.parse_args()

system = System()


# Set clock domain and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set mem mode and create mumbus
system.mem_mode = "timing"
system.membus = SystemXBar()

# Create a simple X86 Timing CPU
system.cpu = X86MinorCPU()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Cache Setup
system.cache = SimpleCache(size="1kB")

system.cpu.icache_port = system.cache.cpu_side
system.cpu.dcache_port = system.cache.cpu_side
system.cache.mem_side = system.membus.cpu_side_ports


# Create an interrupt controller
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Create a memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ranges = [AddrRange("8GB")]
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Setup a process
system.workload = SEWorkload.init_compatible(args.binary)

process = Process()
process.cmd = [args.binary, args.binary_args]
system.cpu.workload = process
system.cpu.createThreads()

# Create the root
root = Root(full_system=False, system=system)

# Instantiate the system
m5.instantiate()
m5.simulate()
