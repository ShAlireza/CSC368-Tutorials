import sys
import m5
from m5.objects import (
    AddrRange,
    DDR3_1600_8x8,
    MemCtrl,
    Process,
    SEWorkload,
    SrcClockDomain,
    System,
    SystemXBar,
    VoltageDomain,
    X86AtomicSimpleCPU,
    Root,
)

system = System()

# Set clock domain and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set mem mode and create mumbus
system.mem_mode = "atomic"
system.membus = SystemXBar()

# Create a simple X86 Atomic CPU
system.cpu = X86AtomicSimpleCPU()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

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
binary = sys.argv[1] if len(sys.argv) > 1 else None
if not binary:
    binary = "/u/csc368h/winter/pub/workloads/hello"

system.workload = SEWorkload.init_compatible(binary)

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Create the root
root = Root(full_system=False, system=system)

# Instantiate the system
m5.instantiate()
m5.simulate()
